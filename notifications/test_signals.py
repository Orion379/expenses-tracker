import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account
from budgets.models import Budget
from categories.models import Category
from expenses.models import Expense
from .models import Notification


class BudgetAlertSignalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alertuser", password="testpass123"
        )
        self.food = Category.objects.create(
            user=self.user, name="Food", color="#F97316"
        )
        self.transport = Category.objects.create(
            user=self.user, name="Transport", color="#2563EB"
        )
        self.account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("10000.00"),
        )
        self.budget = Budget.objects.create(
            user=self.user, category=self.food,
            month=datetime.date(2026, 12, 1),
            limit_amount=Decimal("100.00"),
        )

    def spend(self, amount, category=None, date=None):
        return Expense.objects.create(
            user=self.user,
            category=category or self.food,
            account=self.account,
            title="Test spend",
            amount=Decimal(amount),
            date=date or datetime.date(2026, 12, 5),
        )

    def test_no_budget_means_no_notification(self):
        self.spend("500.00", category=self.transport)
        self.assertEqual(Notification.objects.count(), 0)

    def test_under_80_percent_creates_nothing(self):
        self.spend("79.99")
        self.assertEqual(Notification.objects.count(), 0)

    def test_reaching_80_percent_creates_warning(self):
        self.spend("80.00")
        notification = Notification.objects.get()
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.budget, self.budget)
        self.assertIn("80%", notification.message)
        self.assertFalse(notification.is_read)

    def test_exceeding_budget_creates_alert(self):
        self.spend("100.00")
        notification = Notification.objects.get()
        self.assertIn("exceeded", notification.message)

    def test_warning_is_not_repeated(self):
        self.spend("80.00")
        self.spend("5.00")
        self.assertEqual(Notification.objects.count(), 1)

    def test_warning_then_exceeded_creates_two(self):
        self.spend("80.00")
        self.spend("30.00")
        self.assertEqual(Notification.objects.count(), 2)

    def test_exceeded_alert_is_not_repeated(self):
        self.spend("100.00")
        self.spend("10.00")
        self.assertEqual(Notification.objects.count(), 1)

    def test_other_month_does_not_count(self):
        self.spend("90.00", date=datetime.date(2026, 11, 20))
        self.spend("20.00")
        self.assertEqual(Notification.objects.count(), 0)

    def test_other_category_does_not_count(self):
        self.spend("90.00", category=self.transport)
        self.spend("20.00")
        self.assertEqual(Notification.objects.count(), 0)