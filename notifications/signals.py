from decimal import Decimal

from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from budgets.models import Budget
from expenses.models import Expense
from .models import Notification

WARNING_RATIO = Decimal("0.80")


@receiver(post_save, sender=Expense)
def create_budget_alerts(sender, instance, **kwargs):
    month_start = instance.date.replace(day=1)
    budget = Budget.objects.filter(
        user=instance.user,
        category=instance.category,
        month=month_start,
    ).first()
    if budget is None:
        return

    spent = Expense.objects.filter(
        user=instance.user,
        category=instance.category,
        date__year=month_start.year,
        date__month=month_start.month,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    label = f"{budget.category.name} budget for {month_start:%B %Y}"
    if spent >= budget.limit_amount:
        message = f"You have exceeded your {label}."
    elif spent >= budget.limit_amount * WARNING_RATIO:
        message = f"You have used 80% of your {label}."
    else:
        return

    Notification.objects.get_or_create(
        user=instance.user, budget=budget, message=message
    )