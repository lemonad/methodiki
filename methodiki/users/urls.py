# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.utils import translation


# Switch language temporarily for "static" I18n of URLs
language_for_urls = settings.LANGUAGE_CODE[:2]
language_saved = translation.get_language()
translation.activate(language_for_urls)

urlpatterns = patterns('methodiki.users.views',
    url(r'^$', 'index', name='users-index'),
    # Disallow the corresponding usernames in forms.py if adding URLs here.
    url(r'^(?P<username>.+)$', 'show_user', name='user')
)

# Switch back to the language of choice
translation.activate(language_saved)
