from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
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

    def test_valid_hex_color(self):
        user = get_user_model().objects.create_user(
            username="coloruser",
            password="testpass123"
        )

        category = Category(
            user=user,
            name="Transport",
            color="#2563EB"
        )

        category.full_clean()
        category.save()

        self.assertEqual(category.color, "#2563EB")

    def test_invalid_hex_color(self):
        user = get_user_model().objects.create_user(
            username="invalidcoloruser",
            password="testpass123"
        )

        category = Category(
            user=user,
            name="Food",
            color="banana"
        )

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_name_unique_per_user(self):
        User = get_user_model()

        first_user = User.objects.create_user(
            username="firstuser",
            password="testpass123"
        )

        second_user = User.objects.create_user(
            username="seconduser",
            password="testpass456"
        )

        Category.objects.create(
            user=first_user,
            name="Food",
            color="#F97316"
        )

        duplicate = Category(
            user=first_user,
            name="Food",
            color="#2563EB"
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

        other_category = Category.objects.create(
            user=second_user,
            name="Food",
            color="#16A34A"
        )

        self.assertEqual(other_category.name, "Food")

    def test_category_name_case_insensitive_validation(self):
        user = get_user_model().objects.create_user(
            username="caseuser",
            password="testpass123"
        )

        Category.objects.create(
            user=user,
            name="Food",
            color="#F97316"
        )

        duplicate = Category(
            user=user,
            name="food",
            color="#2563EB"
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_category_name_case_insensitive_database(self):
        user = get_user_model().objects.create_user(
            username="dbcaseuser",
            password="testpass123"
        )

        Category.objects.create(
            user=user,
            name="Food",
            color="#F97316"
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(
                    user=user,
                    name="FOOD",
                    color="#2563EB"
                )


    def test_case_insensitive_names_allowed_for_different_user(self):
        User = get_user_model()

        first_user = User.objects.create_user(
            username="ownerone",
            password="testpass123"
        )

        second_user = User.objects.create_user(
            username="ownertwo",
            password="testpass123"
        )

        Category.objects.create(
            user=first_user,
            name="Food",
            color="#F97316"
        )

        category = Category.objects.create(
            user=second_user,
            name="food",
            color="#2563EB"
        )

        self.assertEqual(category.name, "food")
