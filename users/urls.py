from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path(
        "register/",
         views.register,
         name="register"
         ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            next_page="dashboard"
        ),
        name="login"
    ),
    path(
        "welcome/",
        views.welcome,
        name="welcome"
    ),
    path (
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="users:login"
        ),
        name="logout"
    ),
    path(
        "logout/confirm/",
        login_required(TemplateView.as_view(template_name="logout.html")),
        name="logout_confirm"
    ),
]
