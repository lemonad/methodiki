# -*- coding: utf-8 -*-
from django.forms import ModelForm


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
