from django.core.management import color
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Expense
from accounts.models import Account
from categories.models import Category
from recurring.models import RecurringExpense


# Create your tests here.

class ExpenseModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Amahle",
            password="mahle619",
        )
        self.account = Account.objects.create(
            user=self.user,
            name="Expenses",
            account_type="main",
            balance=Decimal("1000000.00")
        )
        self.category = Category.objects.create(
            user=self.user,
            name="Food",
            color="FF000"
        )
        self.recurring_expense = RecurringExpense.objects.create(
            user=self.user,
            category=self.category,
            account=self.account,
            title="Monthly Subscription",
            amount=Decimal("150000.00"),
            frequency="monthly",
            next_due_date="2026-11-01"
        )
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            account=self.account,
            recurring_expense=self.recurring_expense,
            title="Grocery Shopping",
            amount=Decimal("1000.00"),
            date="2026-08-23",
            note="Weekly groceries"
        )
        
    def test_expense_creation(self):
        saved_expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(saved_expense.title, "Grocery Shopping")
        self.assertEqual(saved_expense.amount, Decimal("1000.00"))
        self.assertEqual(saved_expense.note, "Weekly groceries")
        
    def test_expense_relationship(self):
        self.assertEqual(self.expense.user, self.user)
        self.assertEqual(self.expense.account, self.account)
        self.assertEqual(self.expense.category, self.category)
        
    def test_expense_without_recurring_expense(self):
        expense_without_recurring = Expense.objects.create(
            user=self.user,
            category=self.category,
            account=self.account,
            recurring_expense=None,
            title="Once-off Purchase",
            amount=Decimal(500.00),
            date="2026-01-01",
            note="A once-off expense"
            
        )
        self.assertIsNone(expense_without_recurring.recurring_expense)
    
    def test_expense_recurring_relationship(self):
        self.assertEqual(self.expense.recurring_expense, self.recurring_expense)
        
    def test_expense_string_representation(self):
        expected_result = "Grocery Shopping 1000.00 2026-08-23"
        self.assertEqual(str(self.expense), expected_result)
        
    def test_recurring_expense_deletion_sets_reference_to_null(self):
        self.recurring_expense.delete()
        self.expense.refresh_from_db()
        self.assertIsNone(self.expense.recurring_expense)
    
        
    
       