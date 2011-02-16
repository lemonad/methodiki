# -*- coding: utf-8 -*-
"""
Database settings are in local_settings.py

"""
from settings import *

DEBUG = True
LOCAL_DEVELOPMENT = DEBUG
TEMPLATE_DEBUG = DEBUG

#
# Caching
#
CACHE_BACKEND = 'locmem:///?timeout=60&max_entries=10000'

#
# Whoosh
#
if TESTING:
    HAYSTACK_WHOOSH_STORAGE = 'ram'
else:
    HAYSTACK_WHOOSH_STORAGE = 'file'
    HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'whoosh/dev_index')

try:
    from local_settings import *
except ImportError:
    pass
