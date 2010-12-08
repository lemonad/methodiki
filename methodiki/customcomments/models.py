# -*- coding: utf-8 -*-
from django.contrib.comments.models import Comment
from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _


class CustomComment(Comment):
    lift_method = BooleanField(_("Lift method?"),
                               default=True,
                               blank=True,
                               db_index=True)
