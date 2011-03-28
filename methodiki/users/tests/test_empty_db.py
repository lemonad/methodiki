# -*- coding: utf-8 -*-
"""
Check that users work with empty database.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext


# TODO: Test POSTs!

class UserEmptyDBTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('users-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_show_user(self):
        response = self.client.get(reverse('user',
                                           kwargs={'username':
                                                   'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.failUnlessEqual(response.status_code, 200)

    def test_check_profile(self):
        response = self.client.get(reverse('login-check-profile'))
        next = reverse('login') + "?next=" + reverse('login-check-profile')
        self.assertRedirects(response, next)


class UserEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_index(self):
        response = self.client.get(reverse('users-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_show_user(self):
        response = self.client.get(reverse('user',
                                           kwargs={'username':
                                                   'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertRedirects(response,
                             reverse('methods-frontpage'))

    def test_check_profile(self):
        response = self.client.get(reverse('login-check-profile'))
        self.assertRedirects(response,
                             reverse('methods-frontpage'))
