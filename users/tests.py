from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class RegistrationTests(TestCase):

    def setUp(self):
        self.url = reverse("users:register")

        self.valid_data = {
            "first_name": "Test",
            "last_name": "Person",
            "email": "testperson@example.com",
            "username": "testperson001",
            "password1": "StrongTestPassword#2026",
            "password2": "StrongTestPassword#2026"
        }

    def test_registration_page_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_valid_registration_create_user(self):
        response = self.client.post(
            self.url,
            self.valid_data
        )

        self.assertRedirects(response, self.url)

        User = get_user_model()
        user = User.objects.get(username="testperson001")

        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Person")
        self.assertEqual(
            user.email,
            "testperson@example.com"
        )

        self.assertTrue(
            user.check_password("StrongTestPassword#2026")
        )

        self.assertNotEqual(
            user.password,
            "StrongTestPassword#2026"
        )

    def test_mismatched_passwords_are_rejected(self):
        data = self.valid_data.copy()
        data["password2"] = "DifferentTestPassword#2026"
        response =self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(
            username="testperson001"
            ).exists()
        )

    def test_duplicate_username_is_rejected(self):
        User = get_user_model()

        User.objects.create_user(
            username="testperson001",
            password="ExistingPassword#2026"
        )

        response = self.client.post(
            self.url,
            self.valid_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.filter(
                username="testperson001"
            ).count(),
            1
        )

    def test_first_name_is_required(self):
        data = self.valid_data.copy()
        data["first_name"] = ""

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "first_name",
            response.context["form"].errors
        )
        self.assertFalse(
            get_user_model().objects.filter(
                username="testperson001"
            ).exists()
        )

    def test_last_name_is_required(self):
        data = self.valid_data.copy()
        data["last_name"] = ""

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "last_name",
            response.context["form"].errors
        )
        self.assertFalse(
            get_user_model().objects.filter(
                username="testperson001"
            ).exists()
        )


class AuthenticationTests(TestCase):

    def setUp(self):
        self.username = "testloginuser"
        self.password = "StrongTestPassword#2026"

        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="Test"
        )

        self.login_url = reverse("users:login")
        self.logout_url = reverse("users:logout")
        self.welcome_url = reverse("users:welcome")

    def test_successful_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password
            }
        )

        self.assertRedirects(
            response,
            self.welcome_url
        )

        self.assertIn(
            "_auth_user_id",
            self.client.session
        )

    def test_invalid_password_rejected(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": "WrongPassword123"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

    def test_anonymous_user_cannot_access_welcome(self):
        response = self.client.get(self.welcome_url)

        self.assertRedirects(
            response,
            f"{self.login_url}?next={self.welcome_url}"
        )

    def test_authenticated_user_can_access_welcome(self):
        self.client.force_login(self.user)

        response = self.client.get(self.welcome_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Test")

    def test_logout_ends_session(self):
        self.client.force_login(self.user)

        response = self.client.post(self.logout_url)

        self.assertRedirects(response, self.login_url)

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

        protected_response = self.client.get(
            self.welcome_url
        )

        self.assertRedirects(
            protected_response,
            f"{self.login_url}?next={self.welcome_url}"
        )

    def test_logout_does_not_accept_get(self):
        self.client.force_login(self.user)

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 405)

        self.assertIn(
            "_auth_user_id",
            self.client.session
        )
