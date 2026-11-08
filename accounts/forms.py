from django import forms

from config.crud import OwnedModelForm
from .models import Account

ACCOUNT_TYPES = ["Cash", "Bank", "Mobile wallet", "Savings"]


class AccountForm(OwnedModelForm):
    account_type = forms.ChoiceField(label="Account type", choices=[])

    class Meta:
        model = Account
        fields = ["name", "account_type", "balance"]
        labels = {"name": "Account name", "balance": "Opening balance"}
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Account name"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(t, t) for t in ACCOUNT_TYPES]
        current = self.instance.account_type
        if current and current not in ACCOUNT_TYPES:  # keep older/custom values editable
            choices.append((current, current))
        self.fields["account_type"].choices = [("", "Select account type")] + choices