# -*- coding: utf-8 -*-
"""
Database settings go in local_settings.py

"""
from settings import *


DEBUG = False
LOCAL_DEVELOPMENT = DEBUG
TEMPLATE_DEBUG = DEBUG
MEDIA_DEV_MODE = DEBUG
SEND_BROKEN_LINK_EMAILS = True

#
# Caching
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 3600,
    }
}

#
# Whoosh
#
if TESTING:
    HAYSTACK_WHOOSH_STORAGE = 'ram'
else:
    HAYSTACK_WHOOSH_STORAGE = 'file'
    HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT,
                                        'whoosh/production_index')

try:
    from local_settings import *
except ImportError:
    pass
