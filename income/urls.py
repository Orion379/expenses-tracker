from django.urls import path

from . import views

app_name = "income"

urlpatterns = [
    path("", views.IncomePage.as_view(), name="list"),
    path("<int:pk>/edit/", views.IncomePage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.IncomeDelete.as_view(), name="delete"),
]