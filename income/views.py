from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import IncomeForm
from .models import Income


class IncomePage(OwnedListCreateView):
    model = Income
    form_class = IncomeForm
    template_name = "income.html"
    page = "income"
    singular = "income"
    context_name = "incomes"
    select_related = ("account",)
    order_by = ("-date", "-id")


class IncomeDelete(OwnedDeleteView):
    model = Income
    success_url_name = "income:list"
    singular = "income"