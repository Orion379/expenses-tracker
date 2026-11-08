from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.CategoryPage.as_view(), name="list"),
    path("<int:pk>/edit/", views.CategoryPage.as_view(), name="edit"),
    path("<int:pk>/delete/", views.CategoryDelete.as_view(), name="delete"),
]