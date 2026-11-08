from django import forms

from config.crud import OwnedModelForm
from .models import Category


class CategoryForm(OwnedModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]
        labels = {"name": "Category name", "color": "Color"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category name"}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }