from django import forms
from django.utils import timezone

from config.crud import OwnedModelForm, date_widget
from .models import Income


class IncomeForm(OwnedModelForm):
    owned_fields = ("account",)

    class Meta:
        model = Income
        fields = ["source", "amount", "date", "account"]
        labels = {"source": "Source"}
        widgets = {
            "source": forms.TextInput(attrs={"placeholder": "Income source"}),
            "date": date_widget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = timezone.localdate
        self.fields["account"].empty_label = "Select account"