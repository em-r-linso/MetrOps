from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from unittest.mock import patch

import datetime

from .models import Character


class CharacterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "12345"

        cls.user = get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    @patch(  # mock current time so that it doesn't change while testing
        "django.utils.timezone.now",
        return_value=timezone.datetime(
            2000, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc
        ),  # 2000-01-01 00:00:00
    )
    def test_character_values_set_when_created(self, mock_now):

        character = Character.objects.create(name="Test Character", owner=self.user)

        self.assertEqual(character.owner, self.user)
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.created_at, mock_now.return_value)
        self.assertEqual(character.updated_at, mock_now.return_value)


class ViewTestMixin:
    """Mixin for testing views in the characters app.

    All of the views in this app are for logged in users only, so this mixin
    assumes that guest viewers should get bounced away.
    """

    url = None
    url_name = None
    template_name = None

    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "12345"

        cls.user = get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    def test_view_accessible_when_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_redirect_when_not_logged_in(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            # should redirect to login page
            # "next" should be the page we were trying to access
            f"/accounts/login/?next={reverse(self.url_name)}",
        )


class IndexViewTest(ViewTestMixin, TestCase):
    url = "/characters"
    url_name = "characters:index"
    template_name = "characters/index.html"
