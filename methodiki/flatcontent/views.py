# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, loader


def flatcontent(request, name):
    """ Render a page based on flat content """

    t = loader.get_template('flatcontent.html')
    c = RequestContext(request, {"flat_name": name})
    return HttpResponse(t.render(c))
