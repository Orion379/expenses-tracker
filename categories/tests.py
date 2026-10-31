from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Category


class CategoryModelTests(TestCase):

    def test_category_creation(self):
        user = get_user_model().objects.create_user(
            username= "testuser",
            password= "testpass123"
        )

        category = Category.objects.create(
            user=user,
            name="Food",
            color="#F97316"
        )

        saved_category = Category.objects.get(
            id=category.id
        )

        self.assertEqual(saved_category.name, "Food")
        self.assertEqual(saved_category.color, "#F97316")
        self.assertEqual(saved_category.user, user)
        self.assertEqual(str(saved_category), "Food")

    def test_categorry_ownership(self):
        User = get_user_model()

        first_user = User.objects.create_user(
            username="user1",
            password="testpass123"
        )

        second_user = User.objects.create_user(
            username="user2",
            password="testpass456"
        )

        category = Category.objects.create(
            user=first_user,
            name="Food",
            color="#F97316"
        )

        self.assertTrue(
            Category.objects.filter(
                user=first_user,
                id=category.id
            ).exists()
        )

        self.assertFalse(
            Category.objects.filter(
                user=second_user,
                id=category.id
            ).exists()
        )
