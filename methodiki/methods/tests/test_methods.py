# -*- coding: utf-8 -*-
"""
Tests for methods.

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


class MethodTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def test_is_published(self):
        m = Method.objects.all()[0]
        self.failUnlessEqual(m.is_published(), True)
        self.failUnlessEqual(m.is_draft(), False)

    def test_latest_feed(self):
        response = self.client.get(reverse('methods-feed',
                                   kwargs={'url': 'latest'}))
        self.failUnlessEqual(response.status_code, 200)


class MethodUnauthorizedTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def test_index_unauth(self):
        """ Check that the index page renders. """

        response = self.client.get(reverse('methods-index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_method_views_unauth(self):
        """ Make sure all the views render. """

        methods = Method.objects.exclude(status='DRAFT')
        for method in methods:
            p_at = method.published_at
            response = self.client.get(reverse('methods-show-method',
                                               kwargs={'year': p_at.year,
                                                       'month': p_at.month,
                                                       'day': p_at.day,
                                                       'slug': method.slug}))
            self.failUnlessEqual(response.status_code, 200)

    def test_create_method_view_unauth(self):
        """ Make sure the create method view redirects if not authorized. """

        response = self.client.get(reverse('methods-create-method'))
        self.assertRedirects(response,
                             reverse('login') + "?next=" + \
                             reverse('methods-create-method'),
                             status_code=302,
                             target_status_code=200)

    def test_edit_method_view_unauth(self):
        """ Make sure the edit method view redirects if not authorized. """

        m = Method.objects.all()[0]
        response = self.client.get(reverse('methods-edit-method',
                                           kwargs={'slug': m.slug}))
        self.assertRedirects(response,
                             reverse('login') + "?next=" + \
                             reverse('methods-edit-method',
                                     kwargs={'slug': m.slug}),
                             status_code=302,
                             target_status_code=200)


class MethodAuthorizedTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def setUp(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        self.client.logout()

    def test_index(self):
        """ Check that the index page renders when logged in. """

        response = self.client.get(reverse('methods-index'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['user'].username, 'testclient')

    def test_method_views(self):
        """ Make sure all the views render when logged in. """

        methods = Method.objects.exclude(status='DRAFT')
        for method in methods:
            p_at = method.published_at
            response = self.client.get(reverse('methods-show-method',
                                               kwargs={'year': p_at.year,
                                                       'month': p_at.month,
                                                       'day': p_at.day,
                                                       'slug': method.slug}))
            self.failUnlessEqual(response.status_code, 200)
            self.failUnlessEqual(response.context['user'].username,
                                 'testclient')

    def test_create_method_view(self):
        """ Make sure the create method view renders when logged in. """

        response = self.client.get(reverse('methods-create-method'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'testclient')

    def test_publish_method(self):
        method = Method.objects.filter(status='DRAFT')[0]
        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': method.slug}),
                                    {'publish': "Publish"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)

    def test_diff_method(self):
        method = Method.objects.filter(status='PUBLISHED')[0]

        # Trying to show diff without older revision should fail
        p_at = method.published_at
        response = self.client.get(reverse('methods-diff-method',
                                           kwargs={'year': p_at.year,
                                                   'month': p_at.month,
                                                   'day': p_at.day,
                                                   'slug': method.slug}),
                                   {'diff1': 'latest',
                                    'diff2': 1})
        self.failUnlessEqual(response.status_code, 404)

        # Edit the method, thus creating a revision history entry
        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': method.slug}),
                                    {'method': "Update",
                                     'method-title': "Edited method",
                                     'method-description': "Some text",
                                     'method-editor_comment':
                                          "Updated title"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)
        # Show diff
        response = self.client.get(reverse('methods-diff-method',
                                           kwargs={'year': p_at.year,
                                                   'month': p_at.month,
                                                   'day': p_at.day,
                                                   'slug': method.slug}),
                                   {'diff1': 'latest',
                                    'diff2': 1})
        self.failUnlessEqual(response.status_code, 200)


class EditMethodLoggedInAsNonOwnerTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def setUp(self):
        # Log in as 'user'
        login = self.client.login(username='user', password='password')
        self.failUnless(login, 'Could not log in')

    def test_edit_view_when_method_not_owned_by_logged_in_user(self):
        """
        Make sure the edit method view renders when logged in as
        non-owner of a method.

        """
        # Try to render edit view for method created by another user
        m = Method.objects.get(id=2)
        response = self.client.get(reverse('methods-edit-method',
                                           kwargs={'slug': m.slug}))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_method_owned_by_other_user(self):
        """
        Make sure the edit method form accepts input from a user
        that didn't create the method.

        """
        # Try to post update to own method
        m = Method.objects.get(id=2)
        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': m.slug}),
                                    {'method': "Update",
                                     'method-title': "Hello",
                                     'method-description': "Hello World",
                                     'method-editor_comment':
                                          "Updated title"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)

        m = Method.objects.get(id=2)
        self.failUnlessEqual(m.title, "Hello")


class EditMethodTests(TestCase):
    fixtures = ['users.json',
                'methods.json']

    def setUp(self):
        # Log in as 'user'
        login = self.client.login(username='user', password='password')
        self.failUnless(login, 'Could not log in')

    def test_edit_method_view(self):
        """
        Make sure the edit method view renders when logged in as
        the user who created the method.

        """
        # Should be able to render edit view for own method
        m = Method.objects.get(id=1)
        response = self.client.get(reverse('methods-edit-method',
                                           kwargs={'slug': m.slug}))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_method_by_form(self):
        """ Make sure the edit method form works. """

        # Try to post update to own method
        m = Method.objects.get(id=1)
        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': m.slug}),
                                    {'method': "Update",
                                     'method-title': "Hello",
                                     'method-description': "Hello World",
                                     'method-editor_comment':
                                          "Updated title"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)

        m = Method.objects.get(id=1)
        self.failUnlessEqual(m.title, "Hello")

#    def test_delete_method_by_form(self):
#        """ Delete own method. """
#
#        m = Method.objects.get(id=1)
#        comments = Comment...
#        self.failUnless(comments)
#
#        response = self.client.post(reverse('molnet-polls-edit-poll',
#                                            kwargs={'slug': p.slug}),
#                                    {'delete': "Delete"})
#        self.assertRedirects(response, reverse('molnet-polls-startpage'))
#        self.assertRaises(ObjectDoesNotExist, Poll.objects.get, id=p.id)
#
#        # Verify that choices have been cascade deleted
#        choices_post = Choice.objects.filter(poll=p.id) \
#                                     .values_list('id', flat=True)
#        self.failIf(choices_post)
#
#        # All votes linked to the original choices should have been
#        # cascade deleted
#        votes_post = Vote.objects.filter(choice__in=choices)
#        self.failIf(votes_post)

    def test_publish_method_by_form(self):
        """ Publish own method. """

        m = Method.objects.filter(user__username='user') \
                        .filter(status='DRAFT')[0]

        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': m.slug}),
                                    {'publish': "Publish"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)

        m2 = Method.objects.get(id=m.id)
        self.failUnless(m2.is_published())
        self.failIf(m2.is_draft())

    def test_publish_already_published_method_by_form(self):
        """ Try to publish an already published method. """

        m = Method.objects.filter(user__username='user') \
                        .filter(status='PUBLISHED')[0]

        response = self.client.post(reverse('methods-edit-method',
                                            kwargs={'slug': m.slug}),
                                    {'publish': "Publish"})
        self.assertRedirects(response,
                             reverse('methods-index'),
                             status_code=302,
                             target_status_code=200)

        m2 = Method.objects.get(id=m.id)
        self.failUnless(m2.is_published())
