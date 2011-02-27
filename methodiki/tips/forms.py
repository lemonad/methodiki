# -*- coding: utf-8 -*-
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _

from common.forms import ModelFormRequestUser
from models import Tip


class TipForm(ModelFormRequestUser):
    """ Form for adding and editing tips """

    class Meta:
        model = Tip
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'maxlength': '200',
                                    'style': 'overflow:hidden;'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(TipForm, self).__init__(request, *args, **kwargs)
