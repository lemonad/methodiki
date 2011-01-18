# -*- coding: utf-8 -*-
from datetime import datetime


def lift_method(sender, comment, request, **kwargs):
    # TODO: verify that method owner does not push own method
    if comment.lift_method:
        comment.content_object.last_pushed_at = datetime.now()
        comment.content_object.save()
