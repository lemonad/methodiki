# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import FlatContent


class FlatContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Identifier'),
            {'fields': ('name', 'language_code')}),
        (_('Content'),
            {'fields': ('content',)}),
    )
    list_display = ('name', 'language_code')
    search_fields = ['name', 'content']
    list_filter = ['language_code']

admin.site.register(FlatContent, FlatContentAdmin)
