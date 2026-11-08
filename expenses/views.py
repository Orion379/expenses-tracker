from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import ExpenseForm
from .models import Expense


class ExpensePage(OwnedListCreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses.html"
    page = "expenses"
    singular = "expense"
    context_name = "expenses"
    select_related = ("category", "account")
    order_by = ("-date", "-id")


class ExpenseDelete(OwnedDeleteView):
    model = Expense
    success_url_name = "expenses:list"
    singular = "expense"