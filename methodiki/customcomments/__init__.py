# -*- coding: utf-8 -*-
from django.contrib.comments.models import Comment

from forms import CustomCommentForm
from models import CustomComment


def get_model():
    return CustomComment


def get_form():
    return CustomCommentForm


# FIXME: Remove monkey patching after Django ticket 13411 has been resolved!
#                               (http://code.djangoproject.com/ticket/13411)
# The below is the next_redirect code from Django 1.2.3 with patch
# from ticket 13411 applied
import urllib
from django.contrib.comments.views import utils
from django.core import urlresolvers
from django.http import HttpResponseRedirect

def next_redirect(data, default, default_view, **get_kwargs):
    """
    Handle the "where should I go next?" part of comment views.

    The next value could be a kwarg to the function (``default``), or a
    ``?next=...`` GET arg, or the URL of a given view (``default_view``). See
    the view modules for examples.

    Returns an ``HttpResponseRedirect``.
    """
    next = data.get("next", default)
    if next is None:
        next = urlresolvers.reverse(default_view)
    if get_kwargs:
        if '#' in next:
            tmp = next.rsplit('#', 1)
            next = tmp[0]
            anchor = '#' + tmp[1]
        else:
            anchor = ''

        joiner = ('?' in next) and '&' or '?'
        next += joiner + urllib.urlencode(get_kwargs) + anchor
    return HttpResponseRedirect(next)

# Go monkey patch, go!
utils.next_redirect = next_redirect
