# -*- coding: utf-8 -*-
from django.conf.urls.defaults import handler404, handler500, patterns, url

from feeds import LatestMethods


feeds = {'latest': LatestMethods}

urlpatterns = patterns('methods.views',
    url(r'^$',
        'index',
        name='methods-index'),

    # Methods
    url(r'^new/$',
        'create_method',
        name='methods-create-method'),
    url(r'^edit/(?P<slug>[^\/]+)$',
        'edit_method',
        name='methods-edit-method'),
    url(r'^(?P<id>[0-9]+)/$',
        'show_method_short',
        name='methods-show-method-short'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/'
                                                   '(?P<slug>[^\/]+)/$',
        'show_method',
        name='methods-show-method'),
    url(r'^edit/(?P<slug>[^\/]+)/upload-file$',
        'upload_file',
        name='methods-upload-file'),
    url(r'^edit/(?P<slug>[^\/]+)/delete-file$',
        'delete_file',
        name='methods-delete-file'),

    # Method bonus'
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/'
                                                   '(?P<slug>[^\/]+)/bonus$',
        'show_bonus',
        name='methods-show-bonus'),
    url(r'^bonus/$',
        'create_bonus',
        name='methods-create-bonus'),
    url(r'^bonus/about/$',
        'about_bonus',
        name='methods-about-bonus'),
    url(r'^bonus/(?P<bonus_id>[0-9]+)$',
        'edit_bonus',
        name='methods-edit-bonus'),

    # Tags
    url(r'^tag/(?P<tag_slug>[^\/]+)$',
        'tag_index',
        name='methods-tag-index'),
)

# Feeds
urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        name='methods-feed',
        kwargs={'feed_dict': feeds}),
)
