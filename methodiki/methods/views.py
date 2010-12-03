# -*- coding: utf-8 -*-
import datetime
try:
    import json
except ImportError:
    import simplejson as json
import markdown

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect)
from django.shortcuts import (get_object_or_404, get_list_or_404,
                              render_to_response)
from django.template import Context, RequestContext, loader
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.files import get_thumbnailer

from flatcontent.models import get_flatcontent
from forms import MethodForm
from models import Method, MethodFile


def get_sidebar_methods(user):
    if user.is_authenticated():
        created_by_user = Method.objects.created_by_user(user.id)

        draft_methods_flag = False
        for method in created_by_user:
            if method.status == 'DRAFT':
                draft_methods_flag = True
                break
    else:
        created_by_user = None
        draft_methods_flag = False

    recent_comments = Comment.objects.filter(content_type__model="Method")

    sidebar_methods = {'created_by_user': created_by_user,
                       'recent': Method.objects.recent(),
                       'recent_comments': recent_comments,
                       'draft_methods_flag': draft_methods_flag}
    return sidebar_methods


def get_token(request):
    """
    Returns the the CSRF token required for a POST form. The token is an
    alphanumeric value.

    A side effect of calling this function is to make the the csrf_protect
    decorator and the CsrfViewMiddleware add a CSRF cookie and a
    'Vary: Cookie' header to the outgoing response.  For this reason, you
    may need to use this function lazily, as is done by the csrf
    context processor.

    """
    request.META["CSRF_COOKIE_USED"] = True
    return request.META.get("CSRF_COOKIE", None)


def index(request):
    """ Index page """

    # TODO: Order methods on popularity (see method manager)

    sidebar_methods = get_sidebar_methods(request.user)

    t = loader.get_template('methods-index.html')
    c = RequestContext(request,
                       {'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


def show_method(request, year, month, day, slug):
    form = None
    method = get_object_or_404(Method, slug=slug)

    sidebar_methods = get_sidebar_methods(request.user)

    t = loader.get_template('methods-show-method.html')
    c = RequestContext(request,
                       {'method': method,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


@login_required
def create_method(request):
    preview = {}

    if request.method == 'POST':
        if 'preview' in request.POST:
            form = MethodForm(request, request.POST, prefix='method')
            if form.is_valid():
                preview['title'] = form.cleaned_data['title']
                preview['description'] = form.cleaned_data['description']

        elif 'method' in request.POST:
            form = MethodForm(request, request.POST, prefix='method')
            if form.is_valid():
                m = form.save()
                messages.success(request,
                                 _("Thanks for adding a new method! "
                                   "Don't forget to publish it so it becomes "
                                   "visible to others."))
                return HttpResponseRedirect(reverse('methods-edit-method',
                                                    kwargs={'slug': m.slug}))
        else:
            raise Http404
    else:
        # Initialize form
        method_template = get_flatcontent('method-template')
        form_defaults = {'description': method_template}
        form = MethodForm(request, initial=form_defaults, prefix='method')

    tag_cloud = Method.tags.most_common()

    sidebar_methods = get_sidebar_methods(request.user)

    t = loader.get_template('methods-create-method.html')
    c = RequestContext(request,
                       {'form': form,
                        'tag_cloud': tag_cloud,
                        'preview': preview,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


@login_required
def edit_method(request, slug):
    method = get_object_or_404(Method, slug=slug)
    preview = {}

    if not request.user.is_superuser and request.user != method.user:
        raise PermissionDenied("You must own a method in order to edit it.")

    form = MethodForm(request, instance=method, prefix='method')

    if request.method == 'POST':
        if 'preview' in request.POST:
            form = MethodForm(request,
                              request.POST,
                              instance=method,
                              prefix='method')
            if form.is_valid():
                preview['title'] = form.cleaned_data['title']
                preview['description'] = form.cleaned_data['description']

        elif 'method' in request.POST:
            form = MethodForm(request,
                              request.POST,
                              instance=method,
                              prefix='method')
            if form.is_valid():
                m = form.save()
                if method.is_published():
                    messages.success(request, _("Method saved!"))
                else:
                    messages.success(request, _("Method saved! Don't forget "
                                                "to publish it so it becomes "
                                                "visible to others."))
                return HttpResponseRedirect(reverse('methods-edit-method',
                                                    kwargs={'slug': m.slug}))

        elif 'delete' in request.POST:
            # TODO: Remove associated media
            method.delete()
            messages.success(request, _("Method deleted!"))
            return HttpResponseRedirect(reverse('methods-index'))

        elif 'publish' in request.POST:
            method.status = 'PUBLISHED'
            method.published_at = datetime.datetime.now()
            method.save()
            messages.success(request, _("Method is now published and visible "
                                        "to everyone"))
            return HttpResponseRedirect(reverse('methods-index'))

        elif 'unpublish' in request.POST:
            method.status = 'DRAFT'
            method.save()
            messages.success(request, _("Method is now draft"))
            return HttpResponseRedirect(reverse('methods-edit-method',
                                                kwargs={'slug': method.slug}))
        else:
            raise Http404

    tag_cloud = Method.tags.most_common()
    sidebar_methods = get_sidebar_methods(request.user)
    images = MethodFile.objects.filter(method=method)

    t = loader.get_template('methods-edit-method.html')
    c = RequestContext(request,
                       {'method': method,
                        'tag_cloud': tag_cloud,
                        'preview': preview,
                        'form': form,
                        'images': images,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


@login_required
def upload_file(request, slug):
    """"""
    method = get_object_or_404(Method, slug=slug)

    if request.user != method.user:
        raise PermissionDenied("You must own a method in order to edit it.")

    if request.method == 'POST' and 'qqfile' in request.GET:
        # split filename into name and extension
        split_filename = request.GET['qqfile'].rsplit(".", 1)
        slugified_filename = slugify(split_filename[0])
        if(len(split_filename)) > 1:
            slugified_filename = "%s.%s" % (slugified_filename,
                                            split_filename[1].lower())
        uf = MethodFile(user=request.user, method=method)
        uf.image.save(slugified_filename,
                      ContentFile(request.raw_post_data))
        uf.save()

        # Generate thumbnail
        thumbnail_options = dict(size=(50, 50), crop=True)
        thumbnail = get_thumbnailer(uf.image).get_thumbnail(thumbnail_options)

        thumbnail_options = dict(size=(600, 500))
        resized_image = get_thumbnailer(uf.image) \
                                            .get_thumbnail(thumbnail_options)

        ret_json = {'success': True,
                    'original_url': uf.image.url,
                    'width': uf.width,
                    'height': uf.height,
                    'url': resized_image.url,
                    'thumbnail_url': thumbnail.url}
        return HttpResponse(json.dumps(ret_json))
    else:
        return Http404()


@login_required
def delete_file(request, slug):
    """ Deletes an attached file from a method. """

    method = get_object_or_404(Method, slug=slug)

    if request.user != method.user:
        raise PermissionDenied("You must own a method in order to edit it.")

    if request.method == 'POST' and 'deleteimage' in request.POST:
        image_id = request.POST['deleteimage']
        image = get_object_or_404(MethodFile, id=image_id)

        if image.method.id != method.id:
            raise PermissionDenied("Image does not belong to this method.")

        image.delete()

        if request.is_ajax():
            return HttpResponse(json.dumps({"image_id": image_id}),
                                mimetype="application/json")
        else:
            return Http404()
