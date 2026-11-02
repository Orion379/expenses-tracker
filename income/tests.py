from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal 
from datetime import date

from .models import Income
from accounts.models import Account

# Create your tests here.

class IncomeModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Okuhle",
            password="majobela6"
        )                                        
        
        self.account = Account.objects.create(
            user=self.user,
            name="lifestyle",
            account_type="savings",
            balance=Decimal("150000.00")
            
        )
        
        self.income = Income.objects.create(
            user=self.user,
            account=self.account,
            source="Freelancing",
            amount=Decimal(5000.00),
            date=date(2026, 11, 1)
        )
    def test_income_creation(self):
        saved_income = Income.objects.get(id=self.income.id)

        self.assertEqual(saved_income.source, "Freelancing")
        self.assertEqual(saved_income.amount, Decimal("5000.00"))
        self.assertEqual(saved_income.date, self.income.date)
        
    def test_income_relationship(self):
        self.assertEqual(self.income.user, self.user)
        self.assertEqual(self.income.account, self.account)
        
    def test_income_string_representation(self):
        expected_results = "Freelancing - 5000.00 - lifestyle"