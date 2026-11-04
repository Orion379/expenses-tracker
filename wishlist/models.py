from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class WishlistItem(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PURCHASED = "purchased", "Purchased"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    expense = models.OneToOneField(
        "expenses.Expense",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=200)
    target_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    def clean(self):
        errors = {}
        if self.user_id and self.category_id:
            if self.category.user_id != self.user_id:
                errors["category"] = "Category must belong to the same user."
        if self.user_id and self.expense_id:
            if self.expense.user_id != self.user_id:
                errors["expense"] = "Expense must belong to the same user."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name