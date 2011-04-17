# -*- coding: utf-8 -*-
"""
Model tests for methods.

"""
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext

from ..models import Method, MethodFile


class MethodModelTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def test_method_creation(self):
        now = datetime.now()
        u = User.objects.all()[1]
        m = Method.objects.create(user=u,
                                  last_edited_by=u,
                                  title="I can has cheezburger?",
                                  description="**kthxbye!**",
                                  status='PUBLISHED',
                                  last_pushed_at=now,
                                  published_at=now)

    def test_method_deletion(self):
        m = Method.objects.all()[0]
        m.delete()
        self.assertRaises(ObjectDoesNotExist,
                          Method.objects.get,
                          id=m.id)
