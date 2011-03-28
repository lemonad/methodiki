# -*- coding: utf-8 -*-
"""
Check that tips work with empty database.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext


# TODO: Test POSTs!

class TipEmptyDBTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('tips-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_tip(self):
        response = self.client.get(reverse('tips-edit-tip',
                                           kwargs={'tip_id': 1}))
        next = reverse('login') + \
               "?next=" + \
               reverse('tips-edit-tip', kwargs={'tip_id': 1})
        self.assertRedirects(response, next)


class TipEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_index(self):
        response = self.client.get(reverse('tips-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_tip(self):
        response = self.client.get(reverse('tips-edit-tip',
                                           kwargs={'tip_id': 1}))
        self.failUnlessEqual(response.status_code, 404)
