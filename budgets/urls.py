from django.urls import path

from . import views

app_name = "budgets"

urlpatterns = [
    path("", views.BudgetPage.as_view(), name="list"),
    path("<int:pk>/edit/", views.BudgetPage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.BudgetDelete.as_view(), name="delete"),
]