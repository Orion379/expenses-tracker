from django.urls import path

from . import views

app_name = "recurring"

urlpatterns = [
    path("", views.RecurringPage.as_view(), name="list"),
    path("<int:pk>/edit/", views.RecurringPage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.RecurringDelete.as_view(), name="delete"),
]