from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Account

@transaction.atomic
def adjust_account_balance(*, account_id, user_id, delta):
    """
    Increase or decrease an account balance.
    Positive delta: add money,
    Negative delta: subtract money.
    """

    if not isinstance(delta, Decimal):
        raise TypeError("delta must be a Decimal")

    if not delta.is_finite() or delta != delta.quantize(Decimal("0.01")):
        raise ValueError("delta must be a valid amount with at most 2 decimal places")

    updated = Account.objects.filter(
        pk=account_id,
        user_id=user_id
    ).update(
        balance=F("balance") + delta
    )

    if updated != 1:
        raise Account.DoesNotExist(
            "Account not found for this user"
        )

    return Account.objects.get(
        pk=account_id,
        user_id=user_id
    )
