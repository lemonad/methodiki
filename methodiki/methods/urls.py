# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import translation

from feeds import LatestMethods


feeds = {'latest': LatestMethods}

# Switch language temporarily for "static" I18n of URLs
language_for_urls = settings.LANGUAGE_CODE[:2]
language_saved = translation.get_language()
translation.activate(language_for_urls)

urlpatterns = patterns('methodiki.methods.views',
    url(r'^$',
        'index',
        name='methods-index'),
    url(r'^new/$',
        'create_method',
        name='methods-create-method'),
    url(r'^edit/(?P<slug>[^\/]+)$',
        'edit_method',
        name='methods-edit-method'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/'
                                    '(?P<day>[0-9]{1,2})/(?P<slug>[^\/]+)/$',
        'show_method',
        name='methods-show-method'),
    url(r'^edit/(?P<slug>[^\/]+)/upload-file$',
        'upload_file',
        name='methods-upload-file'),
    url(r'^edit/(?P<slug>[^\/]+)/delete-file$',
        'delete_file',
        name='methods-delete-file'),
)

# Feeds
urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        name='methods-feed',
        kwargs={'feed_dict': feeds}),
)

# Switch back to the language of choice
translation.activate(language_saved)
