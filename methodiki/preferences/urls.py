#!/usr/bin/python
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler500, url
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import ugettext as _


# Switch language temporarily for "static" I18n of URLs
language_for_urls = settings.LANGUAGE_CODE[:2]
language_saved = translation.get_language()
translation.activate(language_for_urls)

urlpatterns = patterns('preferences.views',
    # Change language
    url(_(r'^language/$'),
        'select_language',
        name='settings-select-language'),
    # Change username, email, etc.
    url(_(r'^account/$'), 'profile', name='settings-account'),
    # Change name, url
    url(_(r'^profile/$'), 'profile', name='settings-profile'),
    # Change password
    # url(_(r'^password/$'), 'profile', name='settings-profile'),
    )

# Switch back to the language of choice
translation.activate(language_saved)
