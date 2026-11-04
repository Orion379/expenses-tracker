import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import Account
from categories.models import Category
from expenses.models import Expense
from .models import WishlistItem


class WishlistItemModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass456"
        )
        self.category = Category.objects.create(
            user=self.user, name="Tech", color="#2563EB"
        )
        self.other_category = Category.objects.create(
            user=self.other_user, name="Tech", color="#16A34A"
        )
        self.account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("1000.00")
        )
        self.other_account = Account.objects.create(
            user=self.other_user, name="Theirs", account_type="bank",
            balance=Decimal("1000.00")
        )
        self.expense = Expense.objects.create(
            user=self.user, category=self.category, account=self.account,
            title="Headphones", amount=Decimal("80.00"),
            date=datetime.date(2026, 11, 1), note=""
        )
        self.other_expense = Expense.objects.create(
            user=self.other_user, category=self.other_category,
            account=self.other_account, title="Keyboard",
            amount=Decimal("50.00"), date=datetime.date(2026, 11, 1), note=""
        )

    def build(self, **overrides):
        data = {
            "user": self.user,
            "category": self.category,
            "name": "Laptop",
            "target_price": Decimal("900.00"),
        }
        data.update(overrides)
        return WishlistItem(**data)

    def test_wishlist_item_creation(self):
        item = self.build(
            expense=self.expense,
            priority=WishlistItem.Priority.HIGH,
            status=WishlistItem.Status.PURCHASED,
        )
        item.full_clean()
        item.save()

        saved = WishlistItem.objects.get(id=item.id)
        self.assertEqual(saved.user, self.user)
        self.assertEqual(saved.category, self.category)
        self.assertEqual(saved.expense, self.expense)
        self.assertEqual(saved.name, "Laptop")
        self.assertEqual(saved.target_price, Decimal("900.00"))
        self.assertEqual(saved.priority, "high")
        self.assertEqual(saved.status, "purchased")
        self.assertEqual(str(saved), "Laptop")

    def test_defaults(self):
        item = self.build()
        item.save()
        self.assertEqual(item.priority, "medium")
        self.assertEqual(item.status, "pending")

    def test_category_and_expense_are_optional(self):
        item = self.build(category=None, expense=None)
        item.full_clean()
        item.save()
        self.assertIsNone(item.category)
        self.assertIsNone(item.expense)

    def test_invalid_priority_rejected(self):
        item = self.build(priority="urgent")
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_invalid_status_rejected(self):
        item = self.build(status="shipped")
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_zero_and_negative_target_price_rejected(self):
        for bad_price in [Decimal("0.00"), Decimal("-10.00")]:
            with self.subTest(price=bad_price):
                item = self.build(target_price=bad_price)
                with self.assertRaises(ValidationError):
                    item.full_clean()

    def test_expense_can_only_be_linked_once(self):
        self.build(expense=self.expense).save()
        duplicate = self.build(name="Second wish", expense=self.expense)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate.save()

    def test_deleting_category_keeps_item(self):
        # Uses a fresh category: self.category is RESTRICTed by the expense
        spare = Category.objects.create(
            user=self.user, name="Spare", color="#F97316"
        )
        item = self.build(category=spare)
        item.save()
        spare.delete()
        item.refresh_from_db()
        self.assertIsNone(item.category)

    def test_deleting_expense_keeps_item(self):
        item = self.build(expense=self.expense)
        item.save()
        self.expense.delete()
        item.refresh_from_db()
        self.assertIsNone(item.expense)

    def test_deleting_user_deletes_items(self):
        self.build().save()
        self.user.delete()
        self.assertEqual(WishlistItem.objects.filter(name="Laptop").count(), 0)

    def test_other_users_category_rejected(self):
        item = self.build(category=self.other_category)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_other_users_expense_rejected(self):
        item = self.build(expense=self.other_expense)
        with self.assertRaises(ValidationError):
            item.full_clean()