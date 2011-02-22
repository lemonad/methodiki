# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.utils import translation


# Switch language temporarily for "static" I18n of URLs
language_for_urls = settings.LANGUAGE_CODE[:2]
language_saved = translation.get_language()
translation.activate(language_for_urls)

urlpatterns = patterns('tips.views',
    url(r'^$', 'index', name='tips-index'),
    url(_(r'^(?P<tip_id>[0-9]+)/edit$'), 'edit_tip', name='tips-edit-tip'),
)

# Switch back to the language of choice
translation.activate(language_saved)
