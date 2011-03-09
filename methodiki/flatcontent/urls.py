# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('flatcontent.views',
    url(r'^(?P<name>.+)$', 'flatcontent', name='flatcontent'),
)
