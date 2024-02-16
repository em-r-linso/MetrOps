from django.test import TestCase
from django.urls import reverse


class HomepageTests(TestCase):

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("core:homepage"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("core:homepage"))
        self.assertTemplateUsed(response, "core/homepage.html")
