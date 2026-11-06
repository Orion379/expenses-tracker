import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account
from categories.models import Category
from expenses.models import Expense
from .models import WishlistItem


class WishlistSignalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="wishuser", password="testpass123"
        )
        category = Category.objects.create(
            user=self.user, name="Tech", color="#2563EB"
        )
        account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("1000.00"),
        )
        self.expense = Expense.objects.create(
            user=self.user, category=category, account=account,
            title="Laptop", amount=Decimal("800.00"),
            date=datetime.date(2026, 11, 1),
        )

    def test_item_without_expense_stays_pending(self):
        item = WishlistItem.objects.create(
            user=self.user, name="Laptop", target_price=Decimal("900.00")
        )
        self.assertEqual(item.status, "pending")

    def test_linking_expense_marks_item_purchased(self):
        item = WishlistItem.objects.create(
            user=self.user, name="Laptop", target_price=Decimal("900.00")
        )
        item.expense = self.expense
        item.save()
        item.refresh_from_db()
        self.assertEqual(item.status, "purchased")