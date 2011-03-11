# -*- coding: utf-8 -*-
from django.conf.urls.defaults import handler404, handler500, patterns, url


urlpatterns = patterns('flatcontent.views',
    url(r'^(?P<name>.+)$', 'flatcontent', name='flatcontent'),
)
