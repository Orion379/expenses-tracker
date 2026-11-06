import datetime
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from accounts.models import Account
from categories.models import Category
from expenses.models import Expense
from .models import RecurringExpense
from .processing import next_due_date, process_due_recurring_expenses


class RecurringProcessingTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="recuruser", password="testpass123"
        )
        self.category = Category.objects.create(
            user=self.user, name="Rent", color="#2563EB"
        )
        self.account = Account.objects.create(
            user=self.user, name="Main", account_type="bank",
            balance=Decimal("10000.00"),
        )

    def make(self, due, frequency="monthly"):
        return RecurringExpense.objects.create(
            user=self.user, category=self.category, account=self.account,
            title="Rent", amount=Decimal("500.00"),
            frequency=frequency, next_due_date=due,
        )

    def test_due_expense_is_created_and_date_advances(self):
        recurring = self.make(datetime.date(2026, 12, 1))
        created = process_due_recurring_expenses(today=datetime.date(2026, 12, 1))
        self.assertEqual(created, 1)
        expense = Expense.objects.get()
        self.assertEqual(expense.recurring_expense, recurring)
        self.assertEqual(expense.amount, Decimal("500.00"))
        self.assertEqual(expense.date, datetime.date(2026, 12, 1))
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.account, self.account)
        recurring.refresh_from_db()
        self.assertEqual(recurring.next_due_date, datetime.date(2027, 1, 1))

    def test_not_yet_due_creates_nothing(self):
        self.make(datetime.date(2026, 12, 20))
        created = process_due_recurring_expenses(today=datetime.date(2026, 12, 1))
        self.assertEqual(created, 0)
        self.assertEqual(Expense.objects.count(), 0)

    def test_running_twice_does_not_duplicate(self):
        self.make(datetime.date(2026, 12, 1))
        today = datetime.date(2026, 12, 1)
        process_due_recurring_expenses(today=today)
        second = process_due_recurring_expenses(today=today)
        self.assertEqual(second, 0)
        self.assertEqual(Expense.objects.count(), 1)

    def test_missed_periods_are_caught_up(self):
        recurring = self.make(datetime.date(2026, 10, 1))
        created = process_due_recurring_expenses(today=datetime.date(2026, 12, 15))
        self.assertEqual(created, 3)
        dates = sorted(Expense.objects.values_list("date", flat=True))
        self.assertEqual(dates, [
            datetime.date(2026, 10, 1),
            datetime.date(2026, 11, 1),
            datetime.date(2026, 12, 1),
        ])
        recurring.refresh_from_db()
        self.assertEqual(recurring.next_due_date, datetime.date(2027, 1, 1))

    def test_next_due_date_rules(self):
        self.assertEqual(next_due_date(datetime.date(2026, 12, 1), "weekly"),
                         datetime.date(2026, 12, 8))
        self.assertEqual(next_due_date(datetime.date(2026, 12, 1), "monthly"),
                         datetime.date(2027, 1, 1))
        self.assertEqual(next_due_date(datetime.date(2026, 12, 1), "yearly"),
                         datetime.date(2027, 12, 1))
        self.assertEqual(next_due_date(datetime.date(2027, 1, 31), "monthly"),
                         datetime.date(2027, 2, 28))
        self.assertEqual(next_due_date(datetime.date(2028, 2, 29), "yearly"),
                         datetime.date(2029, 2, 28))

    def test_command_creates_due_expenses(self):
        self.make(timezone.localdate())
        call_command("process_recurring", stdout=StringIO())
        self.assertEqual(Expense.objects.count(), 1)