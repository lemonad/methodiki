# -*- coding: utf-8 -*-
"""
Check that methods works with empty database.

"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote
from django.utils.translation import ugettext


# TODO: Test POSTs!

class MethodEmptyDBTests(TestCase):
    def test_frontpage(self):
        response = self.client.get(reverse('methods-frontpage'))
        self.failUnlessEqual(response.status_code, 200)

    def test_methods_index(self):
        response = self.client.get(reverse('methods-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_create_method(self):
        response = self.client.get(reverse('methods-create-method'))
        next = reverse('login') + "?next=" + reverse('methods-create-method')
        self.assertRedirects(response, next)

    def test_edit_method(self):
        response = self.client.get(reverse('methods-edit-method',
                                           kwargs={'slug': 'does-not-exist'}))
        next = reverse('login') + \
               "?next=" + \
               reverse('methods-edit-method',
                       kwargs={'slug': 'does-not-exist'})
        self.assertRedirects(response, next)

    def test_show_method_short(self):
        response = self.client.get(reverse('methods-show-method-short',
                                           kwargs={'id': 1}))
        self.failUnlessEqual(response.status_code, 404)

    def test_show_method(self):
        response = self.client.get(reverse('methods-show-method',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_upload_file(self):
        response = self.client.get(reverse('methods-upload-file',
                                           kwargs={'slug': 'does-not-exist'}))
        next = reverse('login') + \
               "?next=" + \
               reverse('methods-upload-file',
                       kwargs={'slug': 'does-not-exist'})
        self.assertRedirects(response, next)

    def test_delete_file(self):
        response = self.client.get(reverse('methods-delete-file',
                                           kwargs={'slug': 'does-not-exist'}))
        next = reverse('login') + \
               "?next=" + \
               reverse('methods-delete-file',
                       kwargs={'slug': 'does-not-exist'})
        self.assertRedirects(response, next)

    def test_feed(self):
        response = self.client.get(reverse('methods-feed',
                                           kwargs={'url': 'latest'}))
        self.failUnlessEqual(response.status_code, 200)


class MethodEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_frontpage(self):
        response = self.client.get(reverse('methods-frontpage'))
        self.failUnlessEqual(response.status_code, 200)

    def test_methods_index(self):
        response = self.client.get(reverse('methods-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_create_method(self):
        response = self.client.get(reverse('methods-create-method'))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_method(self):
        response = self.client.get(reverse('methods-edit-method',
                                           kwargs={'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_show_method_short(self):
        response = self.client.get(reverse('methods-show-method-short',
                                           kwargs={'id': 1}))
        self.failUnlessEqual(response.status_code, 404)

    def test_show_method(self):
        response = self.client.get(reverse('methods-show-method',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_upload_file(self):
        response = self.client.get(reverse('methods-upload-file',
                                           kwargs={'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_delete_file(self):
        response = self.client.get(reverse('methods-delete-file',
                                           kwargs={'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_feed(self):
        response = self.client.get(reverse('methods-feed',
                                           kwargs={'url': 'latest'}))
        self.failUnlessEqual(response.status_code, 200)


class MethodBonusEmptyDBTests(TestCase):
    def test_show_bonus(self):
        response = self.client.get(reverse('methods-show-bonus',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_create_bonus(self):
        response = self.client.get(reverse('methods-create-bonus',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist'}))
        next = reverse('login') + \
               "?next=" + \
               reverse('methods-create-bonus',
                       kwargs={'year': 2011,
                               'month': 3,
                               'day': 27,
                               'slug': 'does-not-exist'})
        self.assertRedirects(response, next)

    def test_edit_bonus(self):
        response = self.client.get(reverse('methods-edit-bonus',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist',
                                                   'bonus_id': 1}))
        next = reverse('login') + \
               "?next=" + \
               reverse('methods-edit-bonus',
                       kwargs={'year': 2011,
                               'month': 3,
                               'day': 27,
                               'slug': 'does-not-exist',
                               'bonus_id': 1})
        self.assertRedirects(response, next)


class MethodBonusEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_show_bonus(self):
        response = self.client.get(reverse('methods-show-bonus',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_create_bonus(self):
        response = self.client.get(reverse('methods-create-bonus',
                                           kwargs={'year': '2011',
                                                   'month': '3',
                                                   'day': '27',
                                                   'slug': 'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)

    def test_edit_bonus(self):
        response = self.client.get(reverse('methods-edit-bonus',
                                           kwargs={'year': 2011,
                                                   'month': 3,
                                                   'day': 27,
                                                   'slug': 'does-not-exist',
                                                   'bonus_id': 1}))
        self.failUnlessEqual(response.status_code, 404)


class TagEmptyDBTests(TestCase):
    def test_tags(self):
        response = self.client.get(reverse('methods-tags'))
        self.failUnlessEqual(response.status_code, 200)

    def test_tag_index(self):
        response = self.client.get(reverse('methods-tag-index',
                                           kwargs={'tag_slug':
                                                   'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)


class TagEmptyDBAuthorizedTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_tags(self):
        response = self.client.get(reverse('methods-tags'))
        self.failUnlessEqual(response.status_code, 200)

    def test_tag_index(self):
        response = self.client.get(reverse('methods-tag-index',
                                           kwargs={'tag_slug':
                                                   'does-not-exist'}))
        self.failUnlessEqual(response.status_code, 404)
