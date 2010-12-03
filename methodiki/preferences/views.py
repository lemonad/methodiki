# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _

from forms import ProfileForm


#
# Views
#

@login_required
def select_language(request):
    """Select prefered site language via a form (i18n)."""

    t = loader.get_template('select_language.html')
    c = RequestContext(request, {
        })
    return HttpResponse(t.render(c))


@login_required
def profile(request):
    """ Show/update the logged in user's profile information. """

    profile = request.user.get_profile()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,
                             _("Thanks, your settings have been saved"))
    else:
        form = ProfileForm(instance=profile)

    t = loader.get_template('preferences-profile.html')
    c = RequestContext(request, {"form": form})
    return HttpResponse(t.render(c))


@login_required
def account(request):
    """ Show/update the logged in user's account information. """

    t = loader.get_template('preferences-account.html')
    c = RequestContext(request, {
        })
    return HttpResponse(t.render(c))
