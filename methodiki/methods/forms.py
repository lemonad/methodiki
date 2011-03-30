# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _
from markitup.widgets import MarkItUpWidget
from taggit.forms import TagWidget

from common.forms import ModelFormRequestUser
from models import Method, MethodBonus


class MethodForm(ModelFormRequestUser):
    """ Form for adding and editing methods """

    class Meta:
        model = Method
        fields = ('title', 'description', 'tags')
        widgets = {
            'title': TextInput(attrs={'class': 'span-18 last input'}),
            'description': MarkItUpWidget(auto_preview=False,
                                          attrs={'class':
                                                 'span-18 last input'}),
            'tags': TagWidget(attrs={'class': 'span-18 last input'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(MethodForm, self).__init__(request, *args, **kwargs)

    def clean_tags(self):
        cleaned_tags = self.cleaned_data['tags']
        lowercase_tags = [tag.lower() for tag in cleaned_tags]
        return lowercase_tags


class MethodBonusForm(ModelFormRequestUser):
    """ Form for adding and editing method bonus' """

    class Meta:
        model = MethodBonus
        fields = ('description',)
        widgets = {
            'description': MarkItUpWidget(auto_preview=True,
                                          attrs={'class':
                                                 'span-18 last input'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(MethodBonusForm, self).__init__(request, *args, **kwargs)
