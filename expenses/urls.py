from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.ExpensePage.as_view(), name="list"),
    path("<int:pk>/edit/", views.ExpensePage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ExpenseDelete.as_view(), name="delete"),
]