# -*- coding: utf-8 -*-
from models import Method


def user_methods(request):
    """
    Return number of methods owned by currently logged in user and
    if any of them are draft/unpublished.

    """
    if not request.user.is_authenticated():
        return {}

    user_methods = Method.objects.filter(user=request.user)
    draft_flag = user_methods.exclude(status='PUBLISHED')
    number_of_user_methods = user_methods.count()
    return {"number_of_user_methods": number_of_user_methods,
            "user_methods_draft_flag": draft_flag}
