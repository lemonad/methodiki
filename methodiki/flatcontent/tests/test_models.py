# -*- coding: utf-8 -*-
"""
Model tests for flatcontent.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext

from ..models import FlatContent


class FlatContentModelTests(TestCase):
    fixtures = ['flatcontent.json']

    def setUp(self):
        pass

    def test_flatcontent_creation(self):
        f = FlatContent(name="name",
                        language_code="sv-SE",
                        content=u"Hej världen!")
        f.save()
        fid = f.id
        f = FlatContent.objects.get(id=fid)
        self.failUnlessEqual(f.content, u"Hej världen!")

    def test_flatcontent_deletion(self):
        f = FlatContent.objects.all()[0]
        fid = f.id
        f.delete()
        self.assertRaises(ObjectDoesNotExist,
                          FlatContent.objects.get,
                          id=fid)
