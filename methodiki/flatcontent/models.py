# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import (Manager, Model, CharField, DateField,
                              DateTimeField, FloatField, ForeignKey,
                              ManyToManyField, TextField)
from django.utils import translation
from django.utils.translation import ugettext_lazy as _


class FlatContentManager(Manager):
    pass


class FlatContent(Model):
    """Specific content instance.

    >>> f = FlatContent(name="index-page-welcome-message",
    ...                 language_code="en-US",
    ...                 content="Welcome text goes here.")
    >>> f.save()

    """
    name = CharField(_("Name"),
                     db_index=True,
                     max_length=50)
    language_code = CharField(_("Language code"),
                     db_index=True,
                     max_length=10)
    content = TextField(_("Content"),
                        blank=True)
    objects = FlatContentManager()

    class Meta:
        unique_together = ('name', 'language_code')
        ordering = ['name', 'language_code']
        verbose_name = _("flat content")
        verbose_name_plural = _("flat content")

    def __unicode__(self):
        return self.name


def get_flatcontent(name):
    """ Returns named content in the user's currently selected language.

    If content for that language does not exist, it tries 'en-us'. If that
    fails, returns content regardless of language.

    """
    language_code = translation.get_language()

    content = FlatContent.objects.filter(name__iexact=name) \
                                 .filter(language_code__iexact=language_code)

    if not len(content):
        content = FlatContent.objects.filter(name__iexact=name) \
                                   .filter(language_code__iexact='en-US')

    if not len(content):
        content = FlatContent.objects.filter(name__iexact=name)

    if not len(content):
        return _("No matching content for flat content '%(name)s', "
                 "please use admin interface to create it.") % {'name': name}
    else:
        return content[0].content
