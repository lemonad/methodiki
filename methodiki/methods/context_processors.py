# -*- coding: utf-8 -*-
from models import Method


def user_methods(request):
    """
    Return number of methods owned by currently logged in user and
    if any of them are draft/unpublished.

    """
    if not request.user.is_authenticated():
        return {}

    user_methods = Method.objects.created_by_user(request.user.id)
    user_methods_count = user_methods.count()
    draft_methods = Method.objects.created_by_user_draft(request.user.id)
    draft_flag = draft_methods.count()
    return {"user_methods": user_methods,
            "user_methods_count": user_methods_count,
            "user_methods_draft": draft_methods,
            "user_methods_draft_flag": draft_flag}
