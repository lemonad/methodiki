# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import (handler404, handler500, include,
                                       patterns, url)
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'methods.views.frontpage',
        name="methods-frontpage"),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^metoder/', include('methods.urls')),
    (r'^markitup/', include('markitup.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^settings/', include('preferences.urls')),
    (r'^tips/', include('tips.urls')),
)

# Comments
urlpatterns += patterns('',
    (r'^comments/', include('django.contrib.comments.urls'))
)

# Flat content
urlpatterns += patterns('',
    (r'^flat/', include('flatcontent.urls'))
)

# Login and logout
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$',
        'login',
        {'template_name': 'login.html'},
        name="login"),
    url(r'^login/new-password/$',
        'password_reset',
        {'template_name': 'password_reset_form.html',
         'email_template_name': 'password_reset_email.html'},
        name="password-reset"),
    url(r'^login/new-password/sent/$',
        'password_reset_done',
        {'template_name': 'password_reset_done.html'},
        name="password-reset-done"),
    url(r'^login/new-password/complete/$',
        'password_reset_complete',
        {'template_name': 'password_reset_complete.html'},
        name="password-reset-complete"),
    url(r'^login/new-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+?)/$',
        'password_reset_confirm',
        {'template_name': 'password_reset_confirm.html'},
        name="password-reset-confirm"),

    # Logout
    url(r'^logout/$',
        'logout',
        {'template_name': 'logout.html'},
        name="logout"),
)

# Users + account registering
urlpatterns += patterns('',
    (r'^users/', include('users.urls')),
    url(r'^signup/$',
        'users.views.register',
        name="register"),
    url(r'^login-check-profile/$',
        'users.views.check_profile',
        name="login-check-profile"),
)

# Language
urlpatterns += patterns('',
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT,
             'show_indexes': True}),
    )
