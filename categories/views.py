from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import CategoryForm
from .models import Category


class CategoryPage(OwnedListCreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories.html"
    page = "categories"
    singular = "category"
    context_name = "categories"
    order_by = ("name",)


class CategoryDelete(OwnedDeleteView):
    model = Category
    success_url_name = "categories:list"
    singular = "category"