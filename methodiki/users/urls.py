# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('users.views',
    url(r'^$', 'index', name='users-index'),

    # Disallow the corresponding usernames in forms.py if adding URLs here.
    url(r'^(?P<username>.+)$', 'show_user', name='user')
)
