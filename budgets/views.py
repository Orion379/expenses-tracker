from decimal import Decimal

from django.db.models import Sum

from config.crud import OwnedDeleteView, OwnedListCreateView
from expenses.models import Expense
from .forms import BudgetForm
from .models import Budget


class BudgetPage(OwnedListCreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets.html"
    page = "budgets"
    singular = "budget"
    context_name = "budgets"
    select_related = ("category",)
    order_by = ("-month", "category__name")

    def prepare(self, request, objects):
        for budget in objects:
            spent = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__year=budget.month.year,
                date__month=budget.month.month,
            ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
            budget.spent = spent
            budget.percent_used = int(spent / budget.limit_amount * 100) if budget.limit_amount else 0
        return objects


class BudgetDelete(OwnedDeleteView):
    model = Budget
    success_url_name = "budgets:list"
    singular = "budget"