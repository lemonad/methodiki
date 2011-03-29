# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

    fieldsets = [
        (_("Name"),
         {'fields': ['name']}),
        (_("Avatar"),
         {'fields': ['avatar']})]


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'name', 'email', 'is_staff')
    search_fields = ['username', 'userprofile__name', 'email']

    def name(self, obj):
        return obj.get_profile().name

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
