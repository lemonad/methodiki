# -*- coding: utf-8 -*-
from django.conf.urls.defaults import handler404, handler500, patterns, url


urlpatterns = patterns('tips.views',
    url(r'^$', 'index', name='tips-index'),
    url(r'^(?P<tip_id>[0-9]+)/edit$', 'edit_tip', name='tips-edit-tip'),
)
