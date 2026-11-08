from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.WishlistPage.as_view(), name="list"),
    path("<int:pk>/edit/", views.WishlistPage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.WishlistDelete.as_view(), name="delete"),
]