from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db import transaction


from .taxonomy.generic import ModelWithRequiredTaxon
from .taxonomy.lazy import LazyAppTaxon
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# online ocntent
from django.template import Template, TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates

from localcosmos_server.slugifier import create_unique_slug

from localcosmos_server.online_content.utils import verbosify_template_name

import uuid, os, json, shutil
    

class LocalcosmosUserManager(UserManager):
    
    def create_user(self, username, email, password, **extra_fields):
        slug = create_unique_slug(username, 'slug', self.model)

        extra_fields.update({
            'slug' : slug,
        })

        user = super().create_user(username, email, password, **extra_fields)
        
        return user

    def create_superuser(self, username, email, password, **extra_fields):

        slug = create_unique_slug(username, 'slug', self.model)

        extra_fields.update({
            'slug' : slug,
        })

        superuser = super().create_superuser(username, email, password, **extra_fields)

        return superuser


class LocalcosmosUser(AbstractUser):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = models.SlugField(unique=True)

    details = models.JSONField(null=True)
    
    follows = models.ManyToManyField('self', related_name='followed_by')

    is_banned = models.BooleanField(default=False)

    objects = LocalcosmosUserManager()


    # there is a bug in django for Dataset.user.on_delete=models.SET_NULL (django 3.1)
    # anonymize the datasets here instead of letting django call SET_NULL
    def anonymize_datasets(self):
        from localcosmos_server.datasets.models import Dataset
        datasets = Dataset.objects.filter(user=self)
        for dataset in datasets:
            dataset.user = None

        Dataset.objects.bulk_update(datasets, ['user'])

    # do not alter the delete method
    def delete(self, using=None, keep_parents=False):

        if settings.LOCALCOSMOS_PRIVATE == True:
            self.anonymize_datasets()
            super().delete(using=using, keep_parents=keep_parents)
        else:
            # localcosmos.org uses django-tenants
            from django_tenants.utils import schema_context, get_tenant_model
            Tenant = get_tenant_model()
            
            user_id = self.pk

            # using transactions because multiple schemas can refer to the same
            # user ID as FK references!
            with transaction.atomic():

                deleted = False
                
                # delete user and all of its data across tenants
                for tenant in Tenant.objects.all().exclude(schema_name='public'):
                    with schema_context(tenant.schema_name):

                        self.anonymize_datasets()
                        
                        super().delete(using=using, keep_parents=keep_parents)
                        # reassign the ID because delete() sets it to None
                        self.pk = user_id

                        deleted = True

                
                if deleted == False:
                    
                    # deleting from public schema is not necessary, it happens on the first schema-specific deletion
                    with schema_context('public'):
                        super().delete()
            

    class Meta:
        unique_together = ('email',)


'''
    CLIENTS // DEVICES
    - a client can be used by several users, eg if one logs out and another one logs in on a device
    - the client/user combination is unique
'''
'''
    platform is sent by the platform the app was used on
'''
class UserClients(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'client_id')



'''
    App
    - an App is a webapp which is loaded by an index.html file
    - Apps are served by nginx or apache
'''
class AppManager(models.Manager):

    def create(self, name, primary_language, uid, **kwargs):

        app = self.model(
            name=name,
            primary_language=primary_language,
            uid=uid,
            **kwargs
        )

        app.save()

        return app
    
        
class App(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # this is the app specific subdomain on localcosmos.org/ the unzip folder on lc private
    # unique across all tenants
    uid = models.CharField(max_length=255, unique=True, editable=False)

    # automatically download app updates when you click "publish" on localcosmos.org
    # this feature is not implemented yet
    auto_update = models.BooleanField(default=True)

    primary_language = models.CharField(max_length=15)
    name = models.CharField(max_length=255)

    # the url this app is served at according to your nginx/apache setup
    # online content uses this to load a preview on the LC private installation
    url = models.URLField(null=True)

    # url for downloading the currently released apk
    apk_url = models.URLField(null=True)

    # url for downloading the currently released ipa
    # as of 2019 this does not make any sense, because apple does not support ad-hoc installations
    # for companies < 100 employees
    ipa_url = models.URLField(null=True)

    # COMMERCIAL ONLY
    # url for downloading the current webapp for installing on the private server
    pwa_zip_url = models.URLField(null=True)

    # COMMERCIAL ONLY ?
    # for version comparisons, version of the app in the appkit, version of apk, ipa and webapp might differ
    published_version = models.IntegerField(null=True)

    # an asbolute path on disk to a folder containing a www folder with static index.html file
    # online content uses published_version_path if LOCALCOSMOS_PRIVATE == True
    # online content reads templates and config files from disk
    # usually, published_version_path is settings.LOCALCOSMOS_APPS_ROOT/{App.uid}/published/www/
    # make sure published_version_path is served by your nginx/apache
    published_version_path = models.CharField(max_length=255, null=True)

    # COMMERCIAL ONLY
    # an asbolute path on disk to a folder containing a www folder with static index.html file
    # online content uses preview_version_path if LOCALCOSMOS_PRIVATE == False
    # online content reads templates and config files from disk
    # usually, preview_version_path is settings.LOCALCOSMOS_APPS_ROOT/{App.uid}/preview/www/
    # make sure preview_version_path is served by your nginx/apache
    preview_version_path = models.CharField(max_length=255, null=True)

    # COMMERCIAL ONLY
    # an asbolute path on disk to a folder containing a www folder with static index.html file
    # usually, review_version_path is settings.LOCALCOSMOS_APPS_ROOT/{App.uid}/review/www/
    # make sure review_version_path is served by your nginx/apache
    # review_version_path is used by the localcosmos_server api
    review_version_path = models.CharField(max_length=255, null=True)
    

    objects = AppManager()

    # path where the user uploads app stuff to
    # eg onlince content templates
    @property
    def media_base_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.uid)


    def get_url(self):
        if settings.LOCALCOSMOS_PRIVATE == True:
            return self.url

        # commercial installation uses subdomains
        from django_tenants.utils import get_tenant_domain_model
        Domain = get_tenant_domain_model()
        
        domain = Domain.objects.get(app=self)
        return domain.domain

    def get_admin_url(self):
        if settings.LOCALCOSMOS_PRIVATE == True:
            return reverse('appadmin:home', kwargs={'app_uid':self.uid})

        # commercial installation uses subdomains
        from django_tenants.utils import get_tenant_domain_model
        Domain = get_tenant_domain_model()
        
        domain = Domain.objects.get(app=self)
        path = reverse('appadmin:home', kwargs={'app_uid':self.uid}, urlconf='localcosmos_server.urls')

        url = '{0}{1}'.format(domain.domain, path)
        return url

    # preview is used by online content on the commercial installation only
    # on lc private, preview url is the live url
    def get_preview_url(self):
        if settings.LOCALCOSMOS_PRIVATE == True:
            return self.url

        from django_tenants.utils import get_tenant_domain_model
        Domain = get_tenant_domain_model()
        
        domain = Domain.objects.filter(tenant__schema_name='public').first()
        return '{0}.preview.{1}/'.format(self.uid, domain.domain)


    def get_installed_app_path(self, app_state):

        if settings.LOCALCOSMOS_PRIVATE == True:
            app_state = 'published'

        if app_state == 'published':
            root = self.published_version_path

            # on the first build, there is no published_version_path, but only a review_version_path
            # the "review apk" is exactly the same as the later "published apk",
            # so fall back to review settings if no published settings are available
            if root == None and settings.LOCALCOSMOS_PRIVATE == False:
                root = self.review_version_path

        elif app_state == 'preview':
            root = self.preview_version_path

        elif app_state == 'review':
            root= self.review_version_path

        else:
            raise ValueError('Invalid app_state: {0}'.format(app_state))
        
        return root

    
    # read app settings from disk, online_content
    # located at /www/settings.json, createb by AppPreviewBuilder or AppReleaseBuilder
    # app_state=='preview' or app_state=='review' are for commercial installation only
    def get_settings(self, app_state='preview'):

        root = self.get_installed_app_path(app_state)
            
        settings_json_path = os.path.join(root, 'settings.json')

        with open(settings_json_path, 'r') as settings_file:
            app_settings = json.loads(settings_file.read())

        return app_settings


    # read app features from disk, only published apps
    # app_state=='preview' or app_state=='review' are for commercial installation only
    # used eg by AppTaxonSearch.py
    def get_features(self, app_state='preview'):

        if app_state == 'preview':
            features = {}

        else:
            root = self.get_installed_app_path(app_state)
            
            features_json_path = os.path.join(root, 'localcosmos', 'features.json')

            with open(features_json_path, 'r') as features_file:
                features = json.loads(features_file.read())

        return features


    def languages(self):
        languages = [self.primary_language]
        secondary_languages = SecondaryAppLanguages.objects.filter(app=self).values_list('language_code', flat=True)
        languages += secondary_languages
        return languages
    
    def secondary_languages(self):
        return SecondaryAppLanguages.objects.filter(app=self).values_list('language_code', flat=True)

    
    ###############################################################################################################
    # online content specific
    # on LOCALCOSMOS_PRIVATE==True app_state is always 'published'
    # on LOCALCOSMOS_PRIVATE==False app_state is always 'preview'

    def get_online_content_app_state(self):

        if settings.LOCALCOSMOS_PRIVATE == True:
            return 'published'

        return 'preview'

    # preview or published, depending on LOCALCOSMOS_PRIVATE
    def get_online_content_templates_path(self):
        
        app_state = self.get_online_content_app_state()

        return os.path.join(self.get_installed_app_path(app_state), 'online_content', 'templates')


    def get_user_uploaded_online_content_templates_path(self):
        return os.path.join(self.media_base_path, 'online_content', 'templates')


    # return the online_content specific app settings
    # called from online_content.api.views and online_content.models.TemplateContentFlagsManager
    def get_online_content_settings(self):

        app_state = self.get_online_content_app_state()
        
        app_settings = self.get_settings(app_state=app_state)

        oc_settings = app_settings.get('online_content', {})
        return oc_settings
    
    # return a list of available templates, always use the preview version,
    # used by eg online_content.forms.CreateTemplateContentForm
    # eg displays a selection in the AppAdmin
    def get_online_content_templates(self, template_type):
            
        templates_path = os.path.join(self.get_online_content_templates_path(), template_type)
        oc_settings = self.get_online_content_settings()
        language = self.primary_language

        templates = []

        # the frontend might not supply online content templates
        if os.path.isdir(templates_path):

            # iterate over templates shipped with the frontend
            for filename in os.listdir(templates_path):

                template_path = '{0}/{1}'.format(template_type, filename)
                verbose_name = template_path

                if template_path in oc_settings['verbose_template_names'] and language in oc_settings['verbose_template_names'][template_path]:
                    verbose_name = oc_settings['verbose_template_names'][template_path][language]

                templates.append((template_path, verbose_name))


        # iterate over user uploaded templates
        user_uploaded_templates_path = os.path.join(self.get_user_uploaded_online_content_templates_path(),
                                                    template_type)
        
        if os.path.isdir(user_uploaded_templates_path):
            for filename in os.listdir(user_uploaded_templates_path):
                template_path = '{0}/{1}'.format(template_type, filename)
                verbose_name = verbosify_template_name(template_path)
                templates.append((template_path, verbose_name))

        return templates


    def get_online_content_template(self, template_name):
        # return an instance of Template
        # Template(contents, origin, origin.template_name, self.engine,)
        # contents is the content of the .html file
        # origin is an Origin instance
        # engine is a template engine
        # Template can be instantiated directly, only with contents

        # templates shipped with frontend
        templates_base_dir = self.get_online_content_templates_path()

        # templates uploaded by user
        user_uploaded_templates_base_dir = self.get_user_uploaded_online_content_templates_path()

        # check if template is shipped with the frontend
        template_path = os.path.join(templates_base_dir, template_name)

        if not os.path.isfile(template_path):

            # if not check if the template was uploaded by the user
            template_path = os.path.join(user_uploaded_templates_base_dir, template_name)

            if not os.path.isfile(template_path):
                msg = 'Online Content Template %s does not exist. Tried: %s' % (template_name, template_path)
                raise TemplateDoesNotExist(msg)
        
        
        params = {
            'NAME' : 'OnlineContentEngine',
            #'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [templates_base_dir, user_uploaded_templates_base_dir],
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'loaders' : [
                    'django.template.loaders.filesystem.Loader',
                ]
            },
        }
        engine = DjangoTemplates(params)

        with open(template_path, encoding=engine.engine.file_charset) as fp:
            contents = fp.read()

        # use the above engine with dirs
        template = Template(contents, engine=engine.engine)
        return template

    # only published app
    def get_locale(self, key, language):
        relpath = 'locales/{0}/plain.json'.format(language)
        locale_path = os.path.join(self.published_version_path, relpath)

        if os.path.isfile(locale_path):
            with open(locale_path, 'r') as f:
                locale = json.loads(f.read())
                return locale.get(key, None)

        return None

    # LC PRIVATE: remove all contents from disk
    def delete(self, *args, **kwargs):
        app_folder = os.path.join(settings.LOCALCOSMOS_APPS_ROOT, self.uid)
        if os.path.isdir(app_folder):
            shutil.rmtree(app_folder)
        super().delete(*args, **kwargs)
        

    def __str__(self):
        return self.name


class SecondaryAppLanguages(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=15)

    class Meta:
        unique_together = ('app', 'language_code')



APP_USER_ROLES = (
    ('admin',_('admin')), # can do everything
    ('expert',_('expert')), # can validate datasets (Expert Review)
)
class AppUserRole(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    role = models.CharField(max_length=60, choices=APP_USER_ROLES)

    def __str__(self):
        return '%s' % (self.role)

    class Meta:
        unique_together = ('user', 'app')
    

'''
    Taxonomic Restrictions
'''
TAXONOMIC_RESTRICTION_TYPES = (
    ('exists', _('exists')),
    ('required', _('required')),
    ('optional', _('optional')),
)
class TaxonomicRestrictionBase(ModelWithRequiredTaxon):

    LazyTaxonClass = LazyAppTaxon

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content = GenericForeignKey('content_type', 'object_id')

    restriction_type = models.CharField(max_length=100, choices=TAXONOMIC_RESTRICTION_TYPES, default='exists')

    def __str__(self):
        return self.taxon_latname

    class Meta:
        abstract = True
        unique_together = ('content_type', 'object_id', 'taxon_latname', 'taxon_author')


class TaxonomicRestriction(TaxonomicRestrictionBase):
    pass
