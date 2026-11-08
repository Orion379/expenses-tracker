from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import RecurringExpenseForm
from .models import RecurringExpense


class RecurringPage(OwnedListCreateView):
    model = RecurringExpense
    form_class = RecurringExpenseForm
    template_name = "recurring.html"
    page = "recurring"
    singular = "recurring expense"
    context_name = "recurring_expenses"
    select_related = ("category", "account")
    order_by = ("next_due_date",)


class RecurringDelete(OwnedDeleteView):
    model = RecurringExpense
    success_url_name = "recurring:list"
    singular = "recurring expense"