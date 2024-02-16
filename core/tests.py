import unittest
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm


class ViewTestMixin:
    url = None
    url_name = None
    template_name = None

    def test_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    # this test fails if test_url_exists_at_desired_location fails
    # it's an annoying dependency, but the alternative is so many try-catches
    def test_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)


class HomepageViewTest(ViewTestMixin, TestCase):
    url = "/"
    url_name = "core:homepage"
    template_name = "core/homepage.html"


class LoginViewTest(ViewTestMixin, TestCase):
    url = "/accounts/login/"
    url_name = "core:login"
    template_name = "registration/login.html"
