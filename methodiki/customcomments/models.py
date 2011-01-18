# -*- coding: utf-8 -*-
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _

from signals import lift_method


class CustomComment(Comment):
    lift_method = BooleanField(_("Lift method?"),
                               default=True,
                               blank=True,
                               db_index=True)

comment_was_posted.connect(lift_method)
