from django import forms
from django.utils import timezone

from config.crud import OwnedModelForm, date_widget
from .models import Expense


class ExpenseForm(OwnedModelForm):
    owned_fields = ("category", "account")

    class Meta:
        model = Expense
        fields = ["title", "amount", "date", "category", "account", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Expense title"}),
            "date": date_widget(),
            "note": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = timezone.localdate
        self.fields["category"].empty_label = "Select category"
        self.fields["account"].empty_label = "Select account"