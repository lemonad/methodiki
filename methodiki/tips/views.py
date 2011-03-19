# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import messages
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

from forms import TipForm
from models import Tip


def index(request):
    """ Tips index page """

    tips = Tip.objects.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = TipForm(request, request.POST)
        if form.is_valid():
            t = form.save()
            messages.success(request, _("Thanks for adding a new tip!"))
            return HttpResponseRedirect(reverse('tips-index'))
    else:
        # Initialize form
        form = TipForm(request)

    t = loader.get_template('tips-index.html')
    c = RequestContext(request,
                       {'tips': tips,
                        'form': form})
    return HttpResponse(t.render(c))


def edit_tip(request, tip_id):
    """ Edits tips """

    tip = get_object_or_404(Tip, id=tip_id)

    if not request.user.is_superuser and request.user != tip.user:
        raise PermissionDenied("You must own a tip in order to edit it.")

    form = TipForm(request, instance=tip)

    if request.method == 'POST':
        if 'post-tip' in request.POST:
            form = TipForm(request,
                           request.POST,
                           instance=tip)
            if form.is_valid():
                t = form.save()
                messages.success(request, _("Tip saved!"))
                return HttpResponseRedirect(reverse('tips-index'))
        elif 'delete-tip' in request.POST:
            tip.delete()
            messages.success(request, _("Tip deleted!"))
            return HttpResponseRedirect(reverse('tips-index'))
        else:
            raise Http404

    t = loader.get_template('tips-edit-tip.html')
    c = RequestContext(request,
                       {'tip': tip,
                        'form': form})
    return HttpResponse(t.render(c))
