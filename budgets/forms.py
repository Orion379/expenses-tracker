from django import forms
from django.utils import timezone

from config.crud import OwnedModelForm
from .models import Budget


class BudgetForm(OwnedModelForm):
    owned_fields = ("category",)

    month = forms.DateField(
        label="Month",
        input_formats=["%Y-%m", "%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "month"}, format="%Y-%m"),
    )

    class Meta:
        model = Budget
        fields = ["month", "limit_amount", "category"]
        labels = {"limit_amount": "Limit amount"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["month"].initial = timezone.localdate
        self.fields["category"].empty_label = "Select category"

    def clean_month(self):
        # A budget always belongs to the 1st of its month.
        return self.cleaned_data["month"].replace(day=1)