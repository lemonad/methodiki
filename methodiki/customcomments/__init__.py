# -*- coding: utf-8 -*-
from django.contrib.comments.models import Comment

from customcomments.forms import CustomCommentForm


def get_form():
    return CustomCommentForm
