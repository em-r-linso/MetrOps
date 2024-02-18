from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Character
from django.utils import timezone
import datetime


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
