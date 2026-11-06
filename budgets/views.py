from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from expenses.models import Expense
from .models import Budget


@login_required
def budget_list(request):
    budgets = list(
        Budget.objects.filter(user=request.user)
        .select_related("category")
        .order_by("-month", "category__name")
    )
    for budget in budgets:
        spent = Expense.objects.filter(
            user=request.user,
            category=budget.category,
            date__year=budget.month.year,
            date__month=budget.month.month,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        budget.spent = spent
        budget.percent_used = int(spent / budget.limit_amount * 100)
    return render(request, "budgets.html", {"budgets": budgets})