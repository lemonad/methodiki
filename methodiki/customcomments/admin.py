# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.comments.models import Comment
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _

from models import CustomComment


class CustomCommentAdmin(admin.ModelAdmin):
    fields = ['comment', 'lift_method', 'submit_date']
    list_display = ['id', 'user_name', 'user_email', 'comment_excerpt',
                    'lift_method', 'submit_date']
    search_fields = ['comment', 'user', 'user_email', 'user_url']

    def comment_excerpt(self, obj):
        return truncate_words(obj.comment, 7)


admin.site.register(CustomComment, CustomCommentAdmin)
