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


class IndexViewTest(ViewTestMixin, TestCase):
    url = "/characters"
    url_name = "characters:index"
    template_name = "characters/index.html"
