import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import RestrictedError
from django.test import TestCase

from accounts.models import Account
from categories.models import Category
from .models import RecurringExpense


class RecurringExpenseModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user, name="Rent", color="#2563EB"
        )
        self.account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("1000.00")
        )

    def build(self, **overrides):
        data = {
            "user": self.user,
            "category": self.category,
            "account": self.account,
            "title": "Apartment rent",
            "amount": Decimal("500.00"),
            "frequency": RecurringExpense.Frequency.MONTHLY,
            "next_due_date": datetime.date(2026, 12, 1),
        }
        data.update(overrides)
        return RecurringExpense(**data)

    def test_recurring_expense_creation(self):
        recurring = self.build()
        recurring.full_clean()
        recurring.save()

        saved = RecurringExpense.objects.get(id=recurring.id)
        self.assertEqual(saved.title, "Apartment rent")
        self.assertEqual(saved.amount, Decimal("500.00"))
        self.assertEqual(saved.frequency, "monthly")
        self.assertEqual(saved.next_due_date, datetime.date(2026, 12, 1))
        self.assertEqual(saved.user, self.user)
        self.assertEqual(str(saved), "Apartment rent")

    def test_default_frequency_is_monthly(self):
        recurring = RecurringExpense(
            user=self.user, category=self.category, account=self.account,
            title="Gym", amount=Decimal("20.00"),
            next_due_date=datetime.date(2026, 12, 1),
        )
        self.assertEqual(recurring.frequency, "monthly")

    def test_invalid_frequency_rejected(self):
        recurring = self.build(frequency="daily")
        with self.assertRaises(ValidationError):
            recurring.full_clean()

    def test_zero_and_negative_amounts_rejected(self):
        for bad_amount in [Decimal("0.00"), Decimal("-5.00")]:
            with self.subTest(amount=bad_amount):
                recurring = self.build(amount=bad_amount)
                with self.assertRaises(ValidationError):
                    recurring.full_clean()

    def test_category_with_recurring_expense_cannot_be_deleted(self):
        self.build().save()
        with self.assertRaises(RestrictedError):
            self.category.delete()

    def test_account_with_recurring_expense_cannot_be_deleted(self):
        self.build().save()
        with self.assertRaises(RestrictedError):
            self.account.delete()

    def test_deleting_user_deletes_everything(self):
        self.build().save()
        self.user.delete()
        self.assertEqual(RecurringExpense.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)

    def test_other_users_category_rejected(self):
        other = get_user_model().objects.create_user(
            username="other", password="testpass456"
        )
        other_category = Category.objects.create(
            user=other, name="Rent", color="#16A34A"
        )
        recurring = self.build(category=other_category)
        with self.assertRaises(ValidationError):
            recurring.full_clean()

    def test_other_users_account_rejected(self):
        other = get_user_model().objects.create_user(
            username="other", password="testpass456"
        )
        other_account = Account.objects.create(
            user=other, name="Theirs", account_type="bank",
            balance=Decimal("10.00")
        )
        recurring = self.build(account=other_account)
        with self.assertRaises(ValidationError):
            recurring.full_clean()