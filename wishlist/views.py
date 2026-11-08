from config.crud import OwnedDeleteView, OwnedListCreateView
from .forms import WishlistItemForm
from .models import WishlistItem


class WishlistPage(OwnedListCreateView):
    model = WishlistItem
    form_class = WishlistItemForm
    template_name = "wishlist.html"
    page = "wishlist"
    singular = "wishlist item"
    context_name = "items"
    select_related = ("category", "expense")
    order_by = ("status", "name")


class WishlistDelete(OwnedDeleteView):
    model = WishlistItem
    success_url_name = "wishlist:list"
    singular = "wishlist item"