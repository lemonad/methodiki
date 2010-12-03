# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm as UCF
from django.contrib.auth.models import User
from django.forms import CharField, EmailField, TextInput, ValidationError
from django.utils.translation import ugettext_lazy as _


disallowed_usernames = ("admin", "administrator", "root",
                        "_", ".", "@", "+", "-")


class UserCreationForm(UCF):
    email = EmailField(label=_("Email"))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].required = False

    def clean_username(self):
        username = self.cleaned_data['username']

        for disallowed in disallowed_usernames:
            if disallowed == username:
                raise ValidationError(_("That user name is not valid."))

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(_("That user name is taken."))

    def clean_password2(self):
        """ Disable password confirmation test. """
        password2 = self.cleaned_data['password2']
        return "password2"

    class Meta:
        model = User
        fields = ('username', 'email')
