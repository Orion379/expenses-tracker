from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your account was created successfully."
            )
            return redirect("users:register")

    else:
        form = RegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )

@login_required
def welcome(request):
    return render(request, "users/welcome.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
