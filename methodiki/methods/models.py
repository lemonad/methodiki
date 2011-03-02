# -*- coding: utf-8 -*-
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db.models import (BooleanField, CharField, Count, DateField,
                              DateTimeField, FileField, ForeignKey,
                              IntegerField, Manager, Model, permalink, Q,
                              TextField, TimeField)
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager


class MethodManager(Manager):
    def created_by_user(self, userid):
        return self.filter(user=userid) \
                   .order_by('-published_at')

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

    def __unicode__(self):
        return self.title

    def is_draft(self):
        return (self.status == 'DRAFT')

    def is_published(self):
        return (self.status != 'DRAFT')

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
                   .order_by('-published_at')


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
