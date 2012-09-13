# -*- coding: utf-8 -*-
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.comments.moderation import moderator
from django.contrib.contenttypes.generic import GenericRelation
from django.db.models import (BooleanField, CharField, Count, DateTimeField,
                              FileField, ForeignKey, IntegerField, Manager,
                              Model, permalink, PositiveIntegerField, Q,
                              TextField)
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager
from taggit.utils import edit_string_for_tags

from customcomments.models import CustomComment
from comment_moderation import EmailOwner


class MethodManager(Manager):
    def published(self):
        return self.exclude(status='DRAFT')

    def created_by_user(self, userid):
        return self.filter(user=userid) \
                   .order_by('-date_created')

    def created_by_user_draft(self, userid):
        return self.filter(user=userid) \
                   .exclude(status='PUBLISHED') \
                   .order_by('-date_created')

    def popular(self):
        """
        Popularity is currently as simple as when methods were
        last pushed.

        """
        return self.exclude(status='DRAFT') \
                   .order_by('-last_pushed_at')

    def pushed(self):
        return self.exclude(status='DRAFT') \
                   .order_by('-last_pushed_at', '-published_at')

    def recent(self):
        return self.exclude(status='DRAFT') \
                   .order_by('-published_at')

    def with_pictures(self):
        methods = MethodFile.objects.values_list('method', flat=True) \
                                    .order_by('method') \
                                    .distinct()
        return self.filter(id__in=list(methods)) \
                   .exclude(status='DRAFT')


class Method(Model):
    STATUS_CHOICES = (('DRAFT', _("Draft")),
                      ('PUBLISHED', _("Published")))

    slug = AutoSlugField(_("Slug"),
                         populate_from='title',
                         editable=False,
                         unique=True,
                         blank=True,
                         max_length=80,
                         db_index=True)
    user = ForeignKey(User,
                      verbose_name=_("Created by"),
                      db_index=True)
    last_edited_by = ForeignKey(User,
                                related_name="+",
                                verbose_name=_("Last edited by"),
                                db_index=True)
    editor_comment = CharField(_(u"Editor comment"),
                               max_length=80,
                               blank=False)
    title = CharField(_("Title"),
                      max_length=140,
                      unique=True)
    description = TextField(_("Description"),
                            blank=True)
    status = CharField(_("Status"),
                       max_length=32,
                       choices=STATUS_CHOICES,
                       default='DRAFT',
                       db_index=True)
    last_pushed_at = DateTimeField(_("Date and time pushed"),
                                   null=True,
                                   blank=True,
                                   db_index=True)
    published_at = DateTimeField(_("Date and time published"),
                                 null=True,
                                 blank=True,
                                 db_index=True)
    date_created = DateTimeField(_("Created (date)"),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_("Modified (date)"),
                                  db_index=True,
                                  auto_now=True)
    objects = MethodManager()
    tags = TaggableManager(blank=True)
    comments = GenericRelation(CustomComment,
                               object_id_field="object_pk",
                               content_type_field="content_type")

    def __unicode__(self):
        return self.title

    def is_draft(self):
        return (self.status == 'DRAFT')

    def is_published(self):
        return (self.status != 'DRAFT')

    @property
    def tags_edit_string(self):
        return edit_string_for_tags(self.tags.all())

    @property
    def revision(self):
        """ So we can use a Method as a MethodRevision. """
        return 'latest'

    @property
    def files(self):
        """ So we can use a Method as a MethodRevision. """
        files_set = self.methodfile_set.values_list('image', flat=True)
        return u'\n'.join(files_set)

    @permalink
    def get_absolute_url(self):
        return ('methods-show-method', (), {
                    'year': self.published_at.year,
                    'month': self.published_at.month,
                    'day': self.published_at.day,
                    'slug': self.slug})

    class Meta:
        ordering = ['-last_pushed_at', '-published_at', '-date_created']
        verbose_name = _("method")
        verbose_name_plural = _("methods")


class MethodFile(Model):
    user = ForeignKey(User,
                      verbose_name=_('User'),
                      db_index=True)
    method = ForeignKey(Method,
                        verbose_name=_('Method'),
                        db_index=True)
    image = ThumbnailerImageField(_('Image'),
                                  upload_to='methods',
                                  height_field='height',
                                  width_field='width',
                                  null=True,
                                  blank=True)
    height = IntegerField(_('Image height'),
                          null=True)
    width = IntegerField(_('Image width'),
                         null=True)
    date_created = DateTimeField(_('Created (date)'),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_('Modified (date)'),
                                  db_index=True,
                                  auto_now=True)

    def __unicode__(self):
        return self.image.url

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('uploaded file')
        verbose_name_plural = _('uploaded files')


class MethodBonusManager(Manager):
    def recent(self):
        return self.exclude(status='DRAFT') \
                   .order_by('-published_at')

    def created_by_user(self, userid):
        return self.filter(user=userid) \
                   .order_by('-date_created')

    def created_by_user_draft(self, userid):
        return self.filter(user=userid) \
                   .exclude(status='PUBLISHED') \
                   .order_by('-date_created')

    def published(self):
        return self.exclude(status='DRAFT')


class MethodBonus(Model):
    STATUS_CHOICES = (('DRAFT', _("Draft")),
                      ('PUBLISHED', _("Published")))

    user = ForeignKey(User,
                      verbose_name=_('User'),
                      db_index=True)
    method = ForeignKey(Method,
                        verbose_name=_('Method'),
                        db_index=True)
    description = TextField(_("Description"),
                            blank=True)
    status = CharField(_("Status"),
                       max_length=32,
                       choices=STATUS_CHOICES,
                       default='DRAFT',
                       db_index=True)
    published_at = DateTimeField(_("Date and time published"),
                                 null=True,
                                 blank=True,
                                 db_index=True)
    date_created = DateTimeField(_('Created (date)'),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_('Modified (date)'),
                                  db_index=True,
                                  auto_now=True)
    objects = MethodBonusManager()

    def __unicode__(self):
        return self.description

    def is_draft(self):
        return (self.status == 'DRAFT')

    def is_published(self):
        return (self.status != 'DRAFT')

    class Meta:
        ordering = ['-published_at', '-date_created']
        verbose_name = _("method bonus")
        verbose_name_plural = _("method bonuses")


class MethodRevisionManager(Manager):
    pass


class MethodRevision(Model):
    """
    The idea is to create a new method revision prior to saving changes
    to the method or related objects (files, tags). In essence, the
    method is the latest revision and method revisions contain old
    data plus information on why, when and by whom it was created in
    the first place (editor comment, revision_date and edited_by).

    """
    method = ForeignKey(Method,
                        verbose_name=_("Method"),
                        db_index=True)
    revision = PositiveIntegerField(_("Revision no."),
                                    default=1,
                                    editable=False,
                                    db_index=True)
    edited_by = ForeignKey(User,
                           verbose_name=_("Edited by"),
                           db_index=True)
    editor_comment = CharField(_(u"Editor comment"),
                               max_length=80,
                               blank=False)
    title = CharField(_("Title"),
                      max_length=140)
    description = TextField(_("Description"),
                            blank=True)
    tags = TextField(_("Tags"),
                     blank=True)
    files = TextField(_("Images"),
                      blank=True)
    revision_date = DateTimeField(_("Date"),
                                  db_index=True,
                                  auto_now_add=True)
    objects = MethodRevisionManager()

    def __unicode__(self):
        return _("Revision %(revno)d") % {'title': self.title,
                                          'revno': self.revision}

    def save(self, *args, **kwargs):
        """ Assign a revision number before saving. """
        if self.id is None:
            try:
                self.revision = MethodRevision.objects \
                                .filter(method=self.method) \
                                .latest().revision + 1
            except self.DoesNotExist:
                self.revision = 1
        super(MethodRevision, self).save(*args, **kwargs)

    @property
    def tags_edit_string(self):
        return self.tags

    class Meta:
        ordering = ['-revision']
        get_latest_by = 'revision'
        verbose_name = _("method revision")
        verbose_name_plural = _("method revisions")


if Method not in moderator._registry:
    moderator.register(Method, EmailOwner)
