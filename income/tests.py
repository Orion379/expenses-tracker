from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.deletion import RestrictedError
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
        
        self.other_user = get_user_model().objects.create_user(
            username="Khanya",
            password="afikile1234"
        )                                     
        
        self.account = Account.objects.create(
            user=self.user,
            name="lifestyle",
            account_type="savings",
            balance=Decimal("150000.00")
            
        )
        
        self.other_account = Account.objects.create(
            user=self.other_user,
            name="Expenses",
            account_type="main",
            balance=Decimal("200000.00")
        )
        
        self.income = Income.objects.create(
            user=self.user,
            account=self.account,
            source="Freelancing",
            amount=Decimal("5000.00"),
            date="2026-11-01"
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
        expected_result= "Freelancing  5000.00 lifestyle"
        self.assertEqual(str(self.income), expected_result)
        
    def test_income_rejects_another_users_account(self):
        income = Income(
            user=self.user,
            account=self.other_account,
            source="freelancing",
            amount=Decimal("15000"),
            date=self.income.date
        )
        with self.assertRaises(ValidationError):
            income.full_clean()
            
    def test_income_rejects_zero_amount(self):
        self.income.amount = Decimal("0.00")
        with self.assertRaises(ValidationError): self.income.full_clean()
        
    def test_income_rejects_negative_amount(self):
        self.income.amount = Decimal("-100.00")
        with self.assertRaises(ValidationError): self.income.full_clean()
        
    def test_account_deletion_is_restricted(self):
        with self.assertRaises(RestrictedError): self.account.delete()
        
    def test_user_deletion_cascades_to_income(self):
        self.user.delete()
        self.assertFalse(Income.objects.filter(id=self.income.id).exists())
        
        