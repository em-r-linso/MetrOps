from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


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


# This is also the base.html test
class HomepageViewTest(ViewTestMixin, TestCase):
    url = "/"
    url_name = "core:homepage"
    template_name = "core/homepage.html"

    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "12345"

        cls.user = get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    def test_username_displayed_when_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, self.username)


class LoginViewTest(ViewTestMixin, TestCase):
    url = "/accounts/login/"
    url_name = "core:login"
    template_name = "registration/login.html"

    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "12345"

        cls.user = get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    def test_redirect_when_login_succeeds(self):
        response = self.client.post(
            reverse(self.url_name),
            {"username": self.username, "password": self.password},
        )
        self.assertRedirects(response, reverse("core:homepage"))

    def test_show_error_when_login_fails(self):
        response = self.client.post(
            reverse(self.url_name),
            {"username": "wrong", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a correct username and password." in response.content.decode()
        )


class LogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "12345"

        cls.user = get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    def test_redirect_when_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("core:logout"))
        self.assertRedirects(response, reverse("core:homepage"))
