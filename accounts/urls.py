from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.AccountPage.as_view(), name="list"),
    path("<int:pk>/edit/", views.AccountPage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AccountDelete.as_view(), name="delete"),
]