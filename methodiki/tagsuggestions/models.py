# -*- coding: utf-8 -*-
from django.db.models import (BooleanField, CharField, DateTimeField,
                              ForeignKey, Model)
from django.utils.translation import ugettext_lazy as _


class TagSuggestionCategory(Model):
    name = CharField(_("Tag category name"),
                      max_length=64,
                      unique=True)
    date_created = DateTimeField(_('Created (date)'),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_('Modified (date)'),
                                  db_index=True,
                                  auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("tag suggestion category")
        verbose_name_plural = _("tag suggestion categories")


class TagSuggestion(Model):
    name = CharField(_("Tag name"),
                     max_length=64,
                     unique=True)
    category = ForeignKey(TagSuggestionCategory,
                          verbose_name=_("Category"),
                          db_index=True)
    show_on_frontpage = BooleanField(_("Show on frontpage?"),
                                     default=False,
                                     blank=True,
                                     db_index=True)
    date_created = DateTimeField(_('Created (date)'),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_('Modified (date)'),
                                  db_index=True,
                                  auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("tag suggestion")
        verbose_name_plural = _("tag suggestions")
