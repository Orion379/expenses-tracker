from django import forms
from django.utils import timezone

from config.crud import OwnedModelForm, date_widget
from .models import RecurringExpense


class RecurringExpenseForm(OwnedModelForm):
    owned_fields = ("category", "account")

    class Meta:
        model = RecurringExpense
        fields = ["title", "amount", "frequency", "next_due_date", "category", "account"]
        labels = {"next_due_date": "Next due date"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Payment title"}),
            "next_due_date": date_widget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["next_due_date"].initial = timezone.localdate
        self.fields["category"].empty_label = "Select category"
        self.fields["account"].empty_label = "Select account"