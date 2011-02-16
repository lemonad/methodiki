# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _

from models import Tip


class TipAdmin(ModelAdmin):
    fields = ['text', 'user']
    list_display = ['get_excerpt', 'user', 'date_created', 'date_modified']
    search_fields = ['text']

    def get_excerpt(self, obj):
        return truncate_words(obj.text, 7)


site.register(Tip, TipAdmin)
