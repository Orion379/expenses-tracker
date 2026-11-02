from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class RecurringExpense(models.Model):
    class Frequency(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.RESTRICT
    )
    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.RESTRICT
    )

    title = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.MONTHLY
    )
    next_due_date = models.DateField()

    def clean(self):
        errors = {}
        if self.user_id and self.category_id:
            if self.category.user_id != self.user_id:
                errors["category"] = "Category must belong to the same user."
        if self.user_id and self.account_id:
            if self.account.user_id != self.user_id:
                errors["account"] = "Account must belong to the same user."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title