# -*- coding: utf-8 -*-
import datetime
try:
    import json
except ImportError:
    import simplejson as json

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.forms import ModelForm
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect)
from django.shortcuts import (get_object_or_404, get_list_or_404,
                              render_to_response)
from django.template import Context, RequestContext, loader
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from methods.models import Method
from tips.models import Tip
from forms import UserCreationForm
from models import UserProfile


def index(request):
    """ Users index page """

    users = User.objects.filter(is_active=True) \
                        .order_by('userprofile__name')

    t = loader.get_template('users-index.html')
    c = RequestContext(request, {'users': users})
    return HttpResponse(t.render(c))


def show_user(request, username):
    """ User page """

    user = get_object_or_404(User, username=username)
    methods = Method.objects.filter(user=user) \
                            .order_by('-date_created')
    tips = Tip.objects.filter(user=user) \
                      .order_by('-date_created')

    t = loader.get_template('users-show-user.html')
    c = RequestContext(request, {'profile': user,
                                 'methods': methods,
                                 'tips': tips})
    return HttpResponse(t.render(c))


def register(request):
    # Only allow not logged users to register new accounts
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('methods-frontpage'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('settings-profile'))
    else:
        form = UserCreationForm()

    t = loader.get_template('register.html')
    c = RequestContext(request,
                       {'form': form})
    return HttpResponse(t.render(c))


@login_required
def check_profile(request):
    """
    After login, checks if profile name has been filled in.

    If not, it redirects to the profile edit page.

    """
    if request.user.get_profile().name:
        return HttpResponseRedirect(reverse('methods-frontpage'))
    else:
        return HttpResponseRedirect(reverse('settings-profile'))


def username_exists_ajax(request):
    if request.method == 'GET' and 'username' in request.GET:
        username = request.GET['username']
        exists = True
        try:
            User.objects.get(username=username)
            exists = False
        except User.DoesNotExist:
            pass

        ret_json = {'exists': exists}
        return HttpResponse(json.dumps(ret_json))
    else:
        raise Http404
