# -*- coding: utf-8 -*-
"""
Check that flatcontent works with empty database.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext


class FlatContentEmptyDBTests(TestCase):
    def test_flatcontent_rendering(self):
        response = self.client.get(reverse('flatcontent',
                                   kwargs={'name': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, u"No matching content")
        self.assertContains(response, u"does-not-exist")


class FlatContentEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_flatcontent_rendering(self):
        response = self.client.get(reverse('flatcontent',
                                   kwargs={'name': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 200)
