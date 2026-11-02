import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import RestrictedError
from django.test import TestCase

from categories.models import Category
from .models import Budget


class BudgetModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user, name="Food", color="#F97316"
        )

    def build(self, **overrides):
        data = {
            "user": self.user,
            "category": self.category,
            "month": datetime.date(2026, 12, 1),
            "limit_amount": Decimal("300.00"),
        }
        data.update(overrides)
        return Budget(**data)

    def test_budget_creation(self):
        budget = self.build()
        budget.full_clean()
        budget.save()

        saved = Budget.objects.get(id=budget.id)
        self.assertEqual(saved.month, datetime.date(2026, 12, 1))
        self.assertEqual(saved.limit_amount, Decimal("300.00"))
        self.assertEqual(saved.user, self.user)
        self.assertEqual(saved.category, self.category)
        self.assertEqual(str(saved), "Food budget for 2026-12")

    def test_month_must_be_first_day(self):
        budget = self.build(month=datetime.date(2026, 12, 15))
        with self.assertRaises(ValidationError):
            budget.full_clean()

    def test_zero_and_negative_limits_rejected(self):
        for bad_amount in [Decimal("0.00"), Decimal("-10.00")]:
            with self.subTest(limit=bad_amount):
                budget = self.build(limit_amount=bad_amount)
                with self.assertRaises(ValidationError):
                    budget.full_clean()

    def test_duplicate_budget_same_month_rejected(self):
        self.build().save()
        duplicate = self.build(limit_amount=Decimal("500.00"))
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate.save()

    def test_same_category_different_month_allowed(self):
        self.build().save()
        other_month = self.build(month=datetime.date(2027, 1, 1))
        other_month.full_clean()
        other_month.save()
        self.assertEqual(Budget.objects.count(), 2)

    def test_other_users_category_rejected(self):
        other = get_user_model().objects.create_user(
            username="other", password="testpass456"
        )
        other_category = Category.objects.create(
            user=other, name="Food", color="#16A34A"
        )
        budget = self.build(category=other_category)
        with self.assertRaises(ValidationError):
            budget.full_clean()

    def test_category_with_budget_cannot_be_deleted(self):
        self.build().save()
        with self.assertRaises(RestrictedError):
            self.category.delete()

    def test_deleting_user_deletes_budgets_and_categories(self):
        self.build().save()
        self.user.delete()
        self.assertEqual(Budget.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)