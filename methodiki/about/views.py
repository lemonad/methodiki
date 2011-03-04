# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _

from flatcontent.models import get_flatcontent


#
# Views
#

def why_methodiki(request):
    """ Show why methodiki? """

    t = loader.get_template('why-methodiki.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def markdown_help(request):
    """ Show detailed markdown help """

    t = loader.get_template('markdown-help.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
