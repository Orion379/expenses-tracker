from django.urls import path

from . import views

app_name = "recurring"
urlpatterns = [
    path("", views.recurring_list, name="list"),
]