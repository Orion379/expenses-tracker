from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Account


class AccountModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_account_creation(self):
        account = Account.objects.create(
            user=self.user,
            name="Practice Wallet",
            account_type="wallet",
            balance=Decimal("50000.00")
        )

        saved_account = Account.objects.get(
            id=account.id
        )

        self.assertEqual(saved_account.name, "Practice Wallet")
        self.assertEqual(saved_account.account_type, "wallet")
        self.assertEqual(saved_account.balance, Decimal("50000.00"))
        self.assertEqual(saved_account.user, self.user)
        self.assertEqual(str(saved_account), "Practice Wallet")

    def test_account_ownership(self):
        other_user = get_user_model().objects.create_user(
            username="anotheruser",
            password="testpass456"
        )

        account = Account.objects.create(
            user=other_user,
            name="Other Wallet",
            account_type="wallet",
            balance=Decimal("10000.00")
        )

        self.assertEqual(account.user, other_user)
        self.assertFalse(
            Account.objects.filter(
                user=self.user,
                id=account.id
            ).exists()
        )
