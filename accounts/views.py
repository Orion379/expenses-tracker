from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import AccountForm
from .models import Account


class AccountPage(OwnedListCreateView):
    model = Account
    form_class = AccountForm
    template_name = "accounts.html"
    page = "accounts"
    singular = "account"
    context_name = "accounts"
    order_by = ("name",)


class AccountDelete(OwnedDeleteView):
    model = Account
    success_url_name = "accounts:list"
    singular = "account"