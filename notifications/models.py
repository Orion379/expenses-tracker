from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    budget = models.ForeignKey(
        "budgets.Budget",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    recurring_expense = models.ForeignKey(
        "recurring.RecurringExpense",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}
        if self.user_id and self.budget_id:
            if self.budget.user_id != self.user_id:
                errors["budget"] = "Budget must belong to the same user."
        if self.user_id and self.recurring_expense_id:
            if self.recurring_expense.user_id != self.user_id:
                errors["recurring_expense"] = (
                    "Recurring expense must belong to the same user."
                )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.message[:50]