# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile


class ProfileForm(ModelForm):
    """ Form for editing a user profile. """

    class Meta:
        model = UserProfile
        fields = ('name', 'avatar')
        widgets = {
            'name': TextInput(attrs={'class': 'span-6 last input'}),
        }
