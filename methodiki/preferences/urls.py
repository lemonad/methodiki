# -*- coding: utf-8 -*-
from django.conf.urls.defaults import handler404, handler500, patterns, url


urlpatterns = patterns('preferences.views',
    # Change language
    url(r'^language/$',
        'select_language',
        name='settings-select-language'),

    # Change username, email, etc.
    url(r'^account/$', 'profile', name='settings-account'),

    # Change name, url
    url(r'^profile/$', 'profile', name='settings-profile'),

    # Change password
    # url(_(r'^password/$'), 'profile', name='settings-profile'),
    )
