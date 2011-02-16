# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site
from django.utils.translation import ugettext_lazy as _

from models import TagSuggestion, TagSuggestionCategory


class TagSuggestionAdmin(ModelAdmin):
    fields = ['name', 'category', 'show_on_frontpage']
    list_display = ['name', 'category', 'show_on_frontpage',
                    'date_created', 'date_modified']
    list_filter = ['category', 'show_on_frontpage']
    search_fields = ['name', 'category']

    def get_excerpt(self, obj):
        return '%s'%(obj.description)

class TagSuggestionCategoryAdmin(ModelAdmin):
    fields = ['name']
    list_display = ['name', 'date_created', 'date_modified']
    search_fields = ['name']


site.register(TagSuggestion, TagSuggestionAdmin)
site.register(TagSuggestionCategory, TagSuggestionCategoryAdmin)
