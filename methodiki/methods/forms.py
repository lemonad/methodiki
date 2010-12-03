# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, TextInput
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from markitup.widgets import MarkItUpWidget
from taggit.forms import TagWidget

from models import Method


class ModelFormRequestUser(ModelForm):
    def __init__(self, request, *args, **varargs):
        self.user = request.user
        super(ModelFormRequestUser, self).__init__(*args, **varargs)

    def save(self, commit=True):
        obj = super(ModelFormRequestUser, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
            self.save_m2m()  # Be careful with ModelForms and commit=False
        return obj


class MethodForm(ModelFormRequestUser):
    """ Form for adding and editing methods. """

    class Meta:
        model = Method
        fields = ('title', 'description', 'tags')
        widgets = {
            'title': TextInput(attrs={'class': 'span-18 last input'}),
            'description': MarkItUpWidget(auto_preview=True,
                                          attrs={'class':
                                                 'span-18 last input'}),
            'tags': TagWidget(attrs={'class': 'span-18 last input'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(MethodForm, self).__init__(request, *args, **kwargs)
