from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import WishlistItem


@login_required
def wishlist_list(request):
    items = (
        WishlistItem.objects.filter(user=request.user)
        .select_related("category", "expense")
        .order_by("status", "-priority", "name")
    )
    return render(request, "wishlist.html", {"items": items})