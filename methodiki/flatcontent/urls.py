# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('flatcontent.views',
    url(r'^(?P<name>.+)$', 'flatcontent', name='flatcontent'),
)
