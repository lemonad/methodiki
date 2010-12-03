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

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'methodiki.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

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

SECRET_KEY = "make-this-unique-and-don't-share-it-with-anybody"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'methodiki.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    # FIXME: Missing in 1.2.3
    # "django.contrib.staticfiles.context_processors.staticfiles",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), "fixtures"),
    os.path.join(os.path.dirname(__file__), "flatcontent/fixtures"),
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
    'taggit',
    'taggit_templatetags',
    # methodiki apps
    'customcomments',
    'flatcontent',
    'methods',
    'preferences',
    'users',
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

# Reverse does not work in settings.py so have to use hardcoded
# internationalized URLs here
LOGIN_REDIRECT_URL = ugettext(r'/settings/profile/')
LOGIN_URL = ugettext(r'/login/')
LOGOUT_URL = ugettext(r'/logout/')

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
MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_SKIN = "markitup/skins/markitup"
MARKITUP_AUTO_PREVIEW = False
MARKITUP_MEDIA_URL = os.path.join(MEDIA_URL, 'javascript')

#
# Django-taggit
#
FORCE_LOWERCASE_TAGS = True

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
if TESTING:
    HAYSTACK_WHOOSH_STORAGE = 'ram'
else:
    HAYSTACK_WHOOSH_STORAGE = 'file'
    HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'whoosh/mysite_index')
