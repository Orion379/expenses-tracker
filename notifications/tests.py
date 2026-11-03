import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Account
from budgets.models import Budget
from categories.models import Category
from recurring.models import RecurringExpense
from .models import Notification


class NotificationModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user, name="Food", color="#F97316"
        )
        self.account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("1000.00")
        )
        self.budget = Budget.objects.create(
            user=self.user, category=self.category,
            month=datetime.date(2026, 12, 1),
            limit_amount=Decimal("300.00"),
        )
        self.recurring = RecurringExpense.objects.create(
            user=self.user, category=self.category, account=self.account,
            title="Rent", amount=Decimal("500.00"),
            frequency=RecurringExpense.Frequency.MONTHLY,
            next_due_date=datetime.date(2026, 12, 1),
        )

    def test_notification_creation(self):
        notification = Notification(
            user=self.user,
            budget=self.budget,
            recurring_expense=self.recurring,
            message="You have used 90% of your Food budget.",
        )
        notification.full_clean()
        notification.save()

        saved = Notification.objects.get(id=notification.id)
        self.assertEqual(saved.user, self.user)
        self.assertEqual(saved.budget, self.budget)
        self.assertEqual(saved.recurring_expense, self.recurring)
        self.assertEqual(saved.message, "You have used 90% of your Food budget.")
        self.assertEqual(str(saved), "You have used 90% of your Food budget.")

    def test_defaults(self):
        notification = Notification.objects.create(
            user=self.user, message="Hello"
        )
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)

    def test_budget_and_recurring_expense_are_optional(self):
        notification = Notification(user=self.user, message="General notice")
        notification.full_clean()
        notification.save()
        self.assertIsNone(notification.budget)
        self.assertIsNone(notification.recurring_expense)

    def test_deleting_budget_keeps_notification(self):
        notification = Notification.objects.create(
            user=self.user, budget=self.budget, message="Budget alert"
        )
        self.budget.delete()
        notification.refresh_from_db()
        self.assertIsNone(notification.budget)

    def test_deleting_recurring_expense_keeps_notification(self):
        notification = Notification.objects.create(
            user=self.user, recurring_expense=self.recurring, message="Due soon"
        )
        self.recurring.delete()
        notification.refresh_from_db()
        self.assertIsNone(notification.recurring_expense)

    def test_deleting_user_deletes_notifications(self):
        Notification.objects.create(
            user=self.user, budget=self.budget, message="Alert"
        )
        self.user.delete()
        self.assertEqual(Notification.objects.count(), 0)

    def test_other_users_budget_rejected(self):
        other = get_user_model().objects.create_user(
            username="other", password="testpass456"
        )
        other_category = Category.objects.create(
            user=other, name="Food", color="#16A34A"
        )
        other_budget = Budget.objects.create(
            user=other, category=other_category,
            month=datetime.date(2026, 12, 1),
            limit_amount=Decimal("100.00"),
        )
        notification = Notification(
            user=self.user, budget=other_budget, message="Wrong owner"
        )
        with self.assertRaises(ValidationError):
            notification.full_clean()

    def test_other_users_recurring_expense_rejected(self):
        other = get_user_model().objects.create_user(
            username="other", password="testpass456"
        )
        other_category = Category.objects.create(
            user=other, name="Rent", color="#16A34A"
        )
        other_account = Account.objects.create(
            user=other, name="Theirs", account_type="bank",
            balance=Decimal("10.00")
        )
        other_recurring = RecurringExpense.objects.create(
            user=other, category=other_category, account=other_account,
            title="Their rent", amount=Decimal("100.00"),
            next_due_date=datetime.date(2026, 12, 1),
        )
        notification = Notification(
            user=self.user, recurring_expense=other_recurring,
            message="Wrong owner",
        )
        with self.assertRaises(ValidationError):
            notification.full_clean()