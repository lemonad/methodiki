# -*- coding: utf-8 -*-
from django.contrib.comments.forms import CommentForm


class CustomCommentForm(CommentForm):
    def __init__(self, target_object, data=None, initial=None):
        super(CustomCommentForm, self).__init__(target_object, data, initial)
        class_str = "span-7 append-8 last input"
        self.fields['name'].widget.attrs['class'] = class_str
        self.fields['email'].widget.attrs['class'] = class_str
        self.fields['url'].widget.attrs['class'] = class_str
        self.fields['comment'].widget.attrs['class'] = "span-10 append-8 " \
                                                       "last input"
