# -*- coding: utf-8 -*-
"""
Check that preferences work with empty database.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext


# TODO: Test POSTs!

class PreferencesEmptyDBTests(TestCase):
    def test_select_language(self):
        response = self.client.get(reverse('settings-select-language'))
        next = reverse('login') + \
               "?next=" + \
               reverse('settings-select-language')
        self.assertRedirects(response, next)

    def test_account(self):
        response = self.client.get(reverse('settings-account'))
        next = reverse('login') + "?next=" + reverse('settings-account')
        self.assertRedirects(response, next)

    def test_profile(self):
        response = self.client.get(reverse('settings-profile'))
        next = reverse('login') + "?next=" + reverse('settings-profile')
        self.assertRedirects(response, next)


class PreferencesEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_select_language(self):
        response = self.client.get(reverse('settings-select-language'))
        self.failUnlessEqual(response.status_code, 200)

    def test_account(self):
        response = self.client.get(reverse('settings-account'))
        self.failUnlessEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get(reverse('settings-profile'))
        self.failUnlessEqual(response.status_code, 200)
