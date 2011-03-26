# -*- coding: utf-8 -*-
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db.models import (BooleanField, CharField, DateTimeField,
                              ForeignKey, Manager, Model, TextField)
from django.utils.translation import ugettext_lazy as _


class TipManager(Manager):
    def created_by_user(self, userid):
        return self.filter(user=userid) \
                   .order_by('-date_created')


class Tip(Model):
    slug = AutoSlugField(_("Slug"),
                         populate_from='text',
                         editable=False,
                         unique=True,
                         blank=True,
                         max_length=50,
                         db_index=True)
    user = ForeignKey(User,
                      verbose_name=_("Created by"),
                      db_index=True)
    text = CharField(_("Text"),
                     max_length=200,
                     unique=True)
    date_created = DateTimeField(_('Created (date)'),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_('Modified (date)'),
                                  db_index=True,
                                  auto_now=True)
    objects = TipManager()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("tip")
        verbose_name_plural = _("tips")
