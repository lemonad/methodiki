# -*- coding: utf-8 -*-
import datetime

from haystack.indexes import *
from haystack import site

from models import Method


class MethodIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField()
    author = CharField(model_attr='user')
    tags = MultiValueField()
    published_at = DateTimeField(model_attr='published_at', null=True)

    def prepare_author(self, obj):
        return "%s" % obj.user.get_profile().name

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_queryset(self):
        """ Used when the entire index for model is updated. """
        return Method.objects.exclude(published_at__isnull=True) \
                             .filter(published_at__lte=
                                     datetime.datetime.now())

    def update_object(self, instance, **kwargs):
        """ Only index published methods. """

        # FIXME: Check future publishing dates
        if instance.published_at:
            self.backend.update(self, [instance])


site.register(Method, MethodIndex)
