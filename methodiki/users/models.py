# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import (CharField, DateTimeField, ForeignKey, Manager,
                              Model)
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class UserProfileManager(Manager):
    pass


class UserProfile(Model):
    """ """

    user = ForeignKey(User,
                      verbose_name=_("User"),
                      unique=True,
                      db_index=True)
    name = CharField(_("Name"),
                     max_length=50)
    avatar = ThumbnailerImageField(_("Avatar"),
                                   upload_to='avatars',
                                   null=True,
                                   blank=True)
    date_created = DateTimeField(_("Created (date)"),
                                 db_index=True,
                                 auto_now_add=True)
    date_modified = DateTimeField(_("Modified (date)"),
                                  db_index=True,
                                  auto_now=True)
    objects = UserProfileManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("user")
        verbose_name_plural = _("users")

import signals
