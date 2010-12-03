# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Method


class MethodAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'tags', 'user',
              'status', 'published_at']
    list_display = ['title', 'user', 'status', 'published_at',
                    'date_created', 'date_modified']
    list_filter = ['status']
    search_fields = ['title', 'description']

admin.site.register(Method, MethodAdmin)
