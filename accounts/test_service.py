from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Account
from .services import adjust_account_balance


class AccountBalanceServiceTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="balance_test_user",
            password="StrongTestPassword#2026"
        )

        self.account = Account.objects.create(
            user=self.user,
            name="Savings",
            account_type="Savings",
            balance=Decimal("50000.00")
        )

    def test_positive_delta_increases_balance(self):
        adjust_account_balance(
            account_id=self.account.id,
            user_id=self.user.id,
            delta=Decimal("20000.00")
        )

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("70000.00")
        )

    def test_negative_delta_decreases_balance(self):
        adjust_account_balance(
            account_id=self.account.id,
            user_id=self.user.id,
            delta=Decimal("-5000.00")
        )

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("45000.00")
        )

    def test_other_user_cannot_modify_account(self):
        other_user = get_user_model().objects.create_user(
            username="another_test_user",
            password="StrongTestPassword#2026"
        )

        with self.assertRaises(Account.DoesNotExist):
            adjust_account_balance(
                account_id=self.account.id,
                user_id=other_user.id,
                delta=Decimal("10000.00")
            )

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("50000.00")
        )

    def test_rejects_float_amount(self):
        with self.assertRaises(TypeError):
            adjust_account_balance(
                account_id=self.account.id,
                user_id=self.user.id,
                delta=100.50
            )

    def test_rejects_excess_decimal_places(self):
        with self.assertRaises(ValueError):
            adjust_account_balance(
                account_id=self.account.id,
                user_id=self.user.id,
                delta=Decimal("10.555")
            )
