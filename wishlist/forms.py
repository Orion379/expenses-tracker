from django import forms

from config.crud import OwnedModelForm
from .models import WishlistItem


class WishlistItemForm(OwnedModelForm):
    owned_fields = ("category",)

    class Meta:
        model = WishlistItem
        fields = ["name", "target_price", "priority", "status", "category"]
        labels = {"name": "Item name", "target_price": "Target price"}
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Item name"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "No category"