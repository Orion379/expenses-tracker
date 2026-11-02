import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.RESTRICT
    )
    month = models.DateField()
    limit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "month"],
                name="unique_budget_per_user_category_month"
            )
        ]

    def clean(self):
        errors = {}
        if self.month and self.month.day != 1:
            errors["month"] = "Month must be the first day of the month."
        if self.user_id and self.category_id:
            if self.category.user_id != self.user_id:
                errors["category"] = "Category must belong to the same user."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.category} budget for {self.month:%Y-%m}"