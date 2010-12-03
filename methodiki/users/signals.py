# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete

from models import UserProfile


def create_userprofile(sender, instance=None, **kwdargs):
    """ Automatically create a userprofile when creating a user. """

    if instance is None or kwdargs.get('raw'):
        return

    userprofile, created = UserProfile.objects.get_or_create(user=instance)
    if created:
        userprofile.save()

post_save.connect(create_userprofile, sender=User)
