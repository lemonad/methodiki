# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site
from django.utils.translation import ugettext_lazy as _

from models import TagSuggestion, TagSuggestionCategory, TagText


class TagSuggestionAdmin(ModelAdmin):
    fields = ['name', 'category', 'show_on_frontpage']
    list_display = ['name', 'category', 'show_on_frontpage',
                    'date_created', 'date_modified']
    list_filter = ['category', 'show_on_frontpage']
    search_fields = ['name', 'category']


class TagSuggestionCategoryAdmin(ModelAdmin):
    fields = ['name']
    list_display = ['name', 'date_created', 'date_modified']
    search_fields = ['name']


class TagTextAdmin(ModelAdmin):
    fields = ['text', 'tag']
    list_display = ['tag', 'date_created', 'date_modified']
    search_fields = ['tag', 'text']


site.register(TagSuggestion, TagSuggestionAdmin)
site.register(TagSuggestionCategory, TagSuggestionCategoryAdmin)
site.register(TagText, TagTextAdmin)
