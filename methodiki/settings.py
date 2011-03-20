import os
import sys

# Set the testing flag when running tests
TESTING = ['manage.py', 'test'] == sys.argv[:2]

# Define dummy ugettext to avoid circular imports
ugettext = lambda s: s

PROJECT_ROOT = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_DOC_ROOT = os.path.join(PROJECT_ROOT, 'media')
ADMIN_MEDIA_PREFIX = '/admin_media/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': 'methodiki.db',
                         'USER': '',
                         'PASSWORD': '',
                         'HOST': '',
                         'PORT': ''}}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sv-se'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # Media middleware has to come first
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'methodiki.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    # FIXME: Missing in 1.2.3
    # "django.contrib.staticfiles.context_processors.staticfiles",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "common.context_processors.site",
    "methods.context_processors.user_methods",
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, "fixtures"),
    os.path.join(PROJECT_ROOT, "flatcontent/fixtures"),
)

INSTALLED_APPS = (
    # Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    # Pip installed
    'easy_thumbnails',
    'haystack',
    'markitup',
    'mediagenerator',
    'south',
    'taggit',
    'taggit_templatetags',
    # methodiki apps
    'common',
    'customcomments',
    'flatcontent',
    'methods',
    'preferences',
    'tagsuggestions',
    'tips',
    'users',
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

LOGIN_REDIRECT_URL = r'/login-check-profile'
LOGIN_URL = r'/login/'
LOGOUT_URL = r'/logout/'

SEND_BROKEN_LINK_EMAILS = False

#
# Caching
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

#
# Comments
#
COMMENTS_APP = 'customcomments'
# Methodiki is assumed to be an intranet application so a limit should
# not be necessary
COMMENT_MAX_LENGTH = 100000


#
# Django-markitup
#
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True,
                                         'extensions': ['autolink']})
MARKITUP_SET = "markitup-markdown-set"
MARKITUP_SKIN = "markitup/skins/simple"
MARKITUP_AUTO_PREVIEW = False
MARKITUP_MEDIA_URL = os.path.join(MEDIA_URL, 'javascript')

#
# Django-mediagenerator
#
MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devstatic/'
PRODUCTION_MEDIA_URL = '/static/'
GLOBAL_MEDIA_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
_base_screen_bundle = (
    'css/blueprint/blueprint/screen.css',
    'css/blueprint/blueprint/src/forms.css',
    'css/blueprint/blueprint/plugins/buttons/screen.css',
    'css/screen.scss',
    'javascript/jquery.fancybox-1.3.4/jquery.fancybox-1.3.4.css',
)
_base_js_bundle = (
    'javascript/modernizr-1.7.min.js',
    'javascript/jquery-1.5.1.min.js',
    'javascript/jquery.corner.js',
    'javascript/jquery.fancybox-1.3.4/jquery.fancybox-1.3.4.pack.js',
)

MEDIA_BUNDLES = (
    # CSS
    ('screen.css',) + _base_screen_bundle,
    ('screen-ie.css',) + _base_screen_bundle
                       + ('css/blueprint/blueprint/ie.css',),
    ('edit-methods.css', 'javascript/jquery-taggit/jquery.taggit.css',
                         'javascript/fileuploader/fileuploader.css',
                         'javascript/markitup/skins/simple/style.css',
                         'javascript/markitup-markdown-set/style.css',),
    ('print.css', 'css/blueprint/blueprint/print.css',
                  'css/print.scss',),
    # Javascript
    ('main.js',) + _base_js_bundle,
    ('main-ie.js',) + ('javascript/html5.js',)
                    + _base_js_bundle,
    ('edit-methods.js', 'javascript/jquery.timers-1.2.js',
                        'javascript/jquery-taggit/jquery.taggit.js',
                        'javascript/fileuploader/fileuploader.js',
                        'javascript/markitup/jquery.markitup.js',
                        'javascript/markitup-markdown-set/set.js',),
)

ROOT_MEDIA_FILTERS = {
    'sass': 'mediagenerator.filters.sass.Sass',
    'scss': 'mediagenerator.filters.sass.Sass',
}

#
# Django-taggit
#
FORCE_LOWERCASE_TAGS = True
TAGGIT_TAGCLOUD_MIN = 12
TAGGIT_TAGCLOUD_MAX = 34

#
# Easy-thumbnails
#
THUMBNAIL_MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'thumbnails')
THUMBNAIL_MEDIA_URL = MEDIA_URL + 'thumbnails/'

#
# Haystack search
#
HAYSTACK_SEARCH_ENGINE = "whoosh"
HAYSTACK_SITECONF = "methodiki.search_sites"
