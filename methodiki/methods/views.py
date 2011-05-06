# -*- coding: utf-8 -*-
import datetime
try:
    import json
except ImportError:
    import simplejson as json

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
from django.template.defaultfilters import escape, linebreaksbr, slugify
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from easy_thumbnails.files import get_thumbnailer
from taggit.models import Tag, TaggedItem
from taggit.utils import edit_string_for_tags
from third_party.google_diff_match_patch import diff_match_patch

from flatcontent.models import get_flatcontent
from tagsuggestions.models import (TagSuggestion, TagSuggestionCategory,
                                   TagText)
from tips.models import Tip
from forms import MethodForm, MethodBonusForm
from models import Method, MethodBonus, MethodFile, MethodRevision


def char_diff(text1, text2):
    """ Return the characters differing between two texts. """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(text1, text2)
    return diffs


def get_html_for_diff(diffs):
    """ Return the HTML for a set of differences. """
    # Delete = -1, insert = 1, equal = 0
    html = []
    for op, text in diffs:
        escaped_text = linebreaksbr(escape(text))
        if op == 1:
            html.append('<ins>' + escaped_text + '</ins>')
        elif op == -1:
            html.append('<del>' + escaped_text + '</del>')
        elif op == 0:
            html.append('<span>' + escaped_text + '</span>')
    return ''.join(html)


def get_sidebar_methods(user):
    recent_methods = Method.objects.recent()
    recent_comments = Comment.objects.filter(content_type__model="method") \
                                     .order_by('-submit_date')
    tips = Tip.objects.order_by('?')

    return {'recent': recent_methods,
            'recent_comments': recent_comments,
            'tips': tips}


def get_suggested_tags(frontpage_only=False, match_actual_tags=True):
    suggested_tags = []
    suggested_tag_categories = TagSuggestionCategory.objects.all()
    for category in suggested_tag_categories:
        suggestions = TagSuggestion.objects.filter(category=category)
        if frontpage_only:
            suggestions = suggestions.filter(show_on_frontpage=True)
        suggestions = suggestions.values_list('name', flat=True)

        if not match_actual_tags:
            suggested_tags.append((category.name, suggestions))
        else:
            # Match suggested tags with actual tags because slugs are needed
            # for linking to tag indexes. Only retrieve tags which have
            # associated methods.
            tags = Tag.objects.annotate(number_of_methods=Count('method')) \
                              .filter(name__in=suggestions) \
                              .filter(number_of_methods__gt=0)

            # Perform explicit case sensitive matching. MySQL doesn't
            # do this unless setting collation to binary.
            # TODO: Verify that switching to binary collation for MySQL
            #       doesn't break other stuff.
            ci_tags = []
            for tag in tags:
                if tag.name in suggestions:
                    ci_tags.append(tag)
            if ci_tags:
                suggested_tags.append((category.name, ci_tags))

    return suggested_tags


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


def frontpage(request):
    """ The frontpage """

    try:
        method = Method.objects.with_pictures() \
                               .order_by('?')[0]
    except IndexError:
        method = None

    popular_tags = Tag.objects.annotate(Count('method')) \
                              .order_by('-method__count')[0:10]

    suggested_tags = get_suggested_tags(frontpage_only=True)

    try:
        tips = Tip.objects.order_by('?')[0]
    except IndexError:
        tips = None

    t = loader.get_template('methods-frontpage.html')
    c = RequestContext(request,
                       {'method': method,
                        'popular_tags': popular_tags,
                        'suggested_tags': suggested_tags,
                        'tips': tips})
    return HttpResponse(t.render(c))


def index(request):
    """ Index page """

    sidebar_methods = get_sidebar_methods(request.user)
    popular_methods = Method.objects.popular()

    suggested_tags = get_suggested_tags()

    t = loader.get_template('methods-index.html')
    c = RequestContext(request,
                       {'methods': popular_methods,
                        'suggested_tags': suggested_tags,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


def tags(request):
    """ Tag cloud for methods """

    sidebar_methods = get_sidebar_methods(request.user)
    tags = Tag.objects.annotate(Count('method')) \
                      .order_by('name')

    t = loader.get_template('methods-tags.html')
    c = RequestContext(request,
                       {'tags': tags,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


def tag_index(request, tag_slug):
    """ Index page for a specific tag """

    sidebar_methods = get_sidebar_methods(request.user)
    tag = get_object_or_404(Tag, slug=tag_slug)
    methods = Method.objects.filter(tags__slug=tag_slug) \
                            .order_by('title')

    t = loader.get_template('methods-tag-index.html')
    c = RequestContext(request,
                       {'tag': tag,
                        'methods': methods,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


def show_method_short(request, id):
    """ Very basic URL shortener for methods """

    method = get_object_or_404(Method, id=id)
    return HttpResponseRedirect(reverse('methods-show-method',
            kwargs={'year': method.published_at.year,
                    'month': method.published_at.month,
                    'day': method.published_at.day,
                    'slug': method.slug}))


def show_method(request, year, month, day, slug):
    """ Shows a method """

    method = get_object_or_404(Method, slug=slug)
    revision_history = MethodRevision.objects.filter(method=method)

    tags_list = method.tags.values_list('name', flat=True)
    try:
        tagtext = TagText.objects.tag_texts_for_tags(tags_list) \
                                 .order_by('?')[0]
    except IndexError:
        tagtext = None

    sidebar_methods = get_sidebar_methods(request.user)

    t = loader.get_template('methods-show-method.html')
    c = RequestContext(request,
                       {'method': method,
                        'tagtext': tagtext,
                        'show_edit_method_link': True,
                        'revision_history': revision_history,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


def diff_method(request, year, month, day, slug):
    """
    Show available diffs for a method and lets the user select
    which revisions to show diff for.

    """
    method = get_object_or_404(Method, slug=slug)
    revisions = MethodRevision.objects.filter(method=method) \
                                      .order_by('-revision')
    show_diff = False

    if (request.method == 'GET' and 'diff1' in request.GET and
                                    'diff2' in request.GET):
        diff1 = request.GET['diff1']
        diff2 = request.GET['diff2']

        if diff1 == 'latest':
            title = method.title
            description = method.description
            tags = method.tags_edit_string
            files = method.files
            editor = method.last_edited_by
            editor_comment = method.editor_comment
            revision = _("latest revision")
        else:
            try:
                revision1 = MethodRevision.objects.get(Q(method=method),
                                                       Q(revision=diff1))
            except:
                raise Http404

            title = revision1.title
            description = revision1.description
            tags = revision1.tags_edit_string
            files = revision1.files
            editor = revision1.edited_by
            editor_comment = revision1.editor_comment
            revision = _("revision %(revno)d") % {'revno':
                                                  revision1.revision}

        try:
            revision2 = MethodRevision.objects.get(Q(method=method),
                                                   Q(revision=diff2))
        except:
            raise Http404

        old_title = revision2.title
        old_description = revision2.description
        old_tags = revision2.tags_edit_string
        old_files = revision2.files
        old_editor = revision2.edited_by
        old_editor_comment = revision2.editor_comment
        old_revision = _("revision %(revno)d") % {'revno':
                                                  revision2.revision}

        if title == old_title:
            diff_title = None
        else:
            diff_title = get_html_for_diff(char_diff(old_title, title))

        if description == old_description:
            diff_description = None
        else:
            diff_description = get_html_for_diff(char_diff(old_description,
                                                           description))

        if tags == old_tags:
            diff_tags = None
        else:
            diff_tags = get_html_for_diff(char_diff(old_tags, tags))

        if files == old_files:
            diff_files = None
        else:
            diff_files = get_html_for_diff(char_diff(old_files, files))

        show_diff = True

    t = loader.get_template('methods-diff-method.html')
    if show_diff:
        c = RequestContext(request,
                           {'method': method,
                            'revisions': revisions,
                            'show_diff': show_diff,
                            'diff1': str(diff1),
                            'diff2': str(diff2),
                            'editor_comment': editor_comment,
                            'old_editor_comment': old_editor_comment,
                            'revision': revision,
                            'old_revision': old_revision,
                            'editor': editor,
                            'old_editor': old_editor,
                            'diff_title': diff_title,
                            'diff_desc': diff_description,
                            'diff_tags': diff_tags,
                            'diff_files': diff_files})
    else:
        c = RequestContext(request,
                           {'method': method,
                            'revisions': revisions,
                            'show_diff': show_diff})

    return HttpResponse(t.render(c))


def show_bonus(request, year, month, day, slug):
    """ Shows bonuses for methods """
    method = get_object_or_404(Method, slug=slug)
    bonuses = method.methodbonus_set.published()

    sidebar_methods = get_sidebar_methods(request.user)

    t = loader.get_template('methods-show-bonus.html')
    c = RequestContext(request,
                       {'method': method,
                        'bonuses': bonuses,
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
        form_defaults = {'description': method_template,
                         'editor_comment': '-'}
        form = MethodForm(request, initial=form_defaults, prefix='method')

    sidebar_methods = get_sidebar_methods(request.user)
    suggested_tags = get_suggested_tags(match_actual_tags=False)

    t = loader.get_template('methods-create-method.html')
    c = RequestContext(request,
                       {'form': form,
                        'preview': preview,
                        'suggested_tags': suggested_tags,
                        'sidebar_methods': sidebar_methods})
    return HttpResponse(t.render(c))


@login_required
def edit_method(request, slug):
    method = get_object_or_404(Method, slug=slug)
    preview = {}

    if method.is_draft():
        form_defaults = {'editor_comment': '-'}
    else:
        form_defaults = {'editor_comment': ''}

    form = MethodForm(request,
                      initial=form_defaults,
                      instance=method,
                      prefix='method')

    if request.method == 'POST':
        if 'preview' in request.POST:
            # In regards to showing a preview, we're only interested in if
            # the title and description fields validates.
            form = MethodForm(request,
                              request.POST,
                              instance=method,
                              prefix='method')
            form.fields['editor_comment'].required = False
            if form.is_valid():
                preview['title'] = form.cleaned_data['title']
                preview['description'] = form.cleaned_data['description']

            # Validate form again
            form = MethodForm(request,
                              request.POST,
                              instance=method,
                              prefix='method')
            form.is_valid()

        elif 'method' in request.POST:
            # Save old attributes for checking changes
            old_title = method.title
            old_description = method.description
            old_tags = method.tags_edit_string
            old_files = method.files
            old_editor_comment = method.editor_comment

            form = MethodForm(request,
                              request.POST,
                              instance=method,
                              prefix='method')
            if form.is_valid():
                m = form.save()
                if method.is_published():
                    # If relevant changes, create revision history entry
                    if (m.title != old_title
                            or m.description != old_description
                            or m.tags_edit_string != old_tags
                            or m.files != old_files):
                        mr = MethodRevision(method=m,
                                            title=old_title,
                                            description=old_description,
                                            edited_by=request.user,
                                            editor_comment=old_editor_comment,
                                            files=old_files,
                                            tags=old_tags)
                        mr.save()

                    messages.success(request, _("Method saved!"))
                    return HttpResponseRedirect(reverse('methods-index'))
                else:
                    messages.success(request, _("Method saved! Don't forget "
                                                "to publish it so it becomes "
                                                "visible to others."))
                    return HttpResponseRedirect(reverse('methods-edit-method',
                                                        kwargs={'slug':
                                                                m.slug}))
            else:
                messages.error(request, _("Could not save method! The form "
                                          "was not filled in correctly (see "
                                          "below)."))

        elif 'delete' in request.POST:
            # Remove associated media
            media = method.methodfile_set.all()
            for m in media:
                m.delete()

            # Also remove method
            method.delete()
            messages.success(request, _("Method deleted!"))
            return HttpResponseRedirect(reverse('methods-index'))

        elif 'publish' in request.POST:
            if method.is_published():
                messages.error(request, _("Method is already public"))
            else:
                method.status = 'PUBLISHED'
                method.published_at = datetime.datetime.now()
                method.last_pushed_at = datetime.datetime.now()
                method.save()
                messages.success(request, _("Method is now published and "
                                            "visible to everyone"))
            return HttpResponseRedirect(reverse('methods-index'))
        else:
            raise Http404

    sidebar_methods = get_sidebar_methods(request.user)
    images = MethodFile.objects.filter(method=method)
    suggested_tags = get_suggested_tags(match_actual_tags=False)

    t = loader.get_template('methods-edit-method.html')
    c = RequestContext(request,
                       {'method': method,
                        'preview': preview,
                        'form': form,
                        'images': images,
                        'sidebar_methods': sidebar_methods,
                        'suggested_tags': suggested_tags})
    return HttpResponse(t.render(c))


@login_required
def create_bonus(request, year, month, day, slug):
    method = get_object_or_404(Method, slug=slug)
    preview = {}

    if request.method == 'POST':
        if 'preview' in request.POST:
            form = MethodBonusForm(request, request.POST, prefix='bonus')
            if form.is_valid():
                preview['description'] = form.cleaned_data['description']

        elif 'bonus' in request.POST:
            form = MethodBonusForm(request, request.POST, prefix='bonus')
            if form.is_valid():
                b = form.save(commit=False)
                b.method = method
                b.save()
                messages.success(request,
                                 _("Thanks for adding a new method bonus! "
                                   "Don't forget to publish it so it becomes "
                                   "visible to others."))
                return HttpResponseRedirect(reverse('methods-edit-bonus',
                    kwargs={'year': method.published_at.year,
                            'month': method.published_at.month,
                            'day': method.published_at.day,
                            'slug': method.slug,
                            'bonus_id': b.id}))
        else:
            raise Http404
    else:
        # Initialize form
        bonus_template = get_flatcontent('bonus-template')
        form_defaults = {'description': bonus_template}
        form = MethodBonusForm(request,
                               initial=form_defaults,
                               prefix='bonus')

    t = loader.get_template('methods-create-bonus.html')
    c = RequestContext(request,
                       {'method': method,
                        'form': form,
                        'preview': preview})
    return HttpResponse(t.render(c))


@login_required
def edit_bonus(request, year, month, day, slug, bonus_id):
    method = get_object_or_404(Method, slug=slug)
    bonus = get_object_or_404(MethodBonus, id=bonus_id)
    preview = {}

    if not request.user.is_superuser and request.user != bonus.user:
        raise PermissionDenied("You must own a method bonus in "
                               "order to edit it.")

    form = MethodBonusForm(request, instance=bonus, prefix='bonus')

    if request.method == 'POST':
        if 'preview' in request.POST:
            form = MethodBonusForm(request,
                                   request.POST,
                                   instance=bonus,
                                   prefix='bonus')
            if form.is_valid():
                preview['description'] = form.cleaned_data['description']

        elif 'bonus' in request.POST:
            form = MethodBonusForm(request,
                                   request.POST,
                                   instance=bonus,
                                   prefix='bonus')
            if form.is_valid():
                b = form.save()
                if bonus.is_published():
                    messages.success(request, _("Bonus saved!"))
                    return HttpResponseRedirect(reverse('methods-show-bonus',
                        kwargs={'year': bonus.method.published_at.year,
                                'month': bonus.method.published_at.month,
                                'day': bonus.method.published_at.day,
                                'slug': bonus.method.slug}))
                else:
                    messages.success(request, _("Bonus saved! Don't forget "
                                                "to publish it so it becomes "
                                                "visible to others."))
                    return HttpResponseRedirect(
                        reverse('methods-edit-bonus',
                            kwargs={'year': bonus.method.published_at.year,
                                    'month': bonus.method.published_at.month,
                                    'day': bonus.method.published_at.day,
                                    'slug': bonus.method.slug,
                                    'bonus_id': bonus.id}))

        elif 'delete' in request.POST:
            bonus.delete()
            messages.success(request, _("Bonus deleted!"))
            return HttpResponseRedirect(reverse('methods-show-bonus',
                kwargs={'year': bonus.method.published_at.year,
                        'month': bonus.method.published_at.month,
                        'day': bonus.method.published_at.day,
                        'slug': bonus.method.slug}))

        elif 'publish' in request.POST:
            if bonus.is_published():
                messages.error(request, _("Bonus is already public"))
            else:
                bonus.status = 'PUBLISHED'
                bonus.published_at = datetime.datetime.now()
                bonus.save()
                messages.success(request, _("Bonus is now published and "
                                            "visible to everyone"))
            return HttpResponseRedirect(reverse('methods-show-bonus',
                kwargs={'year': bonus.method.published_at.year,
                        'month': bonus.method.published_at.month,
                        'day': bonus.method.published_at.day,
                        'slug': bonus.method.slug}))
        else:
            raise Http404

    t = loader.get_template('methods-edit-bonus.html')
    c = RequestContext(request,
                       {'method': method,
                        'bonus': bonus,
                        'preview': preview,
                        'form': form,
                        'edit_bonus_flag': True})
    return HttpResponse(t.render(c))


@login_required
@csrf_exempt
def upload_file(request, slug):
    """
    Handles attaching files to a method.

    File uploads also add to method revision history (currently, only
    the file names are stored and not the actual files).

    """
    method = get_object_or_404(Method, slug=slug)

    if request.method == 'POST':
        if request.is_ajax():
            filename = request.META["HTTP_X_FILE_NAME"]
        else:
            filename = request.FILES['qqfile'].name

        # split filename into name and extension
        split_filename = filename.rsplit(".", 1)
        slugified_filename = slugify(split_filename[0])
        if(len(split_filename)) > 1:
            slugified_filename = "%s.%s" % (slugified_filename,
                                            split_filename[1].lower())

        old_files = method.files

        uf = MethodFile(user=request.user, method=method)
        if request.is_ajax():
            file_content = ContentFile(request.raw_post_data)
        else:
            file_content = ContentFile(request.FILES['qqfile'].read())

        try:
            ret = uf.image.save(slugified_filename, file_content)
        except TypeError:
            # Not an image
            ret_json = {'success': False,
                        'error': ugettext("Error: File is not an image.")}
            return HttpResponse(json.dumps(ret_json))

        ret = uf.save()

        if method.is_published():
            # Create a method revision after adding to method related data
            mr = MethodRevision(method=method,
                                title=method.title,
                                description=method.description,
                                edited_by=request.user,
                                editor_comment="[file added]",
                                tags=method.tags_edit_string,
                                files=old_files)
            mr.save()

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
                    'thumbnail_url': thumbnail.url,
                    'image_id': uf.id}
        return HttpResponse(json.dumps(ret_json))
    else:
        raise Http404


@login_required
def delete_file(request, slug):
    """
    Deletes an attached file from a method.

    File deletions also add to method revision history (currently, only
    the file names are stored and not the actual files).

    """
    method = get_object_or_404(Method, slug=slug)

    if request.method == 'POST' and 'deleteimage' in request.POST:
        image_id = request.POST['deleteimage']
        image = get_object_or_404(MethodFile, id=image_id)

        if image.method.id != method.id:
            raise PermissionDenied("Image does not belong to this method.")

        if method.is_published():
            # Create a method revision before deleting method related data
            mr = MethodRevision(method=method,
                                title=method.title,
                                description=method.description,
                                edited_by=request.user,
                                editor_comment="[file deleted]",
                                tags=method.tags_edit_string,
                                files=method.files)
            mr.save()

        image.delete()

        if request.is_ajax():
            return HttpResponse(json.dumps({"image_id": image_id}),
                                mimetype="application/json")
        else:
            raise Http404
