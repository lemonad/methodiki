# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Method, MethodBonus


class MethodAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'tags', 'user',
              'status', 'published_at', 'last_pushed_at']
    list_display = ['title', 'user', 'status', 'published_at',
                    'last_pushed_at', 'date_created', 'date_modified']
    list_filter = ['status']
    search_fields = ['title', 'description']


class MethodBonusAdmin(admin.ModelAdmin):
    fields = ['description', 'user', 'method',
              'status', 'published_at']
    list_display = ['user', 'method', 'status', 'published_at',
                    'date_created', 'date_modified']
    list_filter = ['status']
    search_fields = ['description']


admin.site.register(Method, MethodAdmin)
admin.site.register(MethodBonus, MethodBonusAdmin)
