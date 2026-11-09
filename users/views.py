from django.contrib.auth.decorators import login_required
from django.contrib import messages
import calendar
from decimal import Decimal
from django.contrib.auth import login

from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.models import Account
from budgets.models import Budget
from config.crud import money
from expenses.models import Expense
from income.models import Income
from .forms import ProfileForm, RegistrationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account was created successfully."
            )
            return redirect("dashboard")

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

def compact_money(value):
    value = float(value)
    if value >= 1_000_000:
        return f"₦{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"₦{value / 1_000:.0f}k"
    return f"₦{value:.0f}"


@login_required
def dashboard(request):
    user = request.user
    today = timezone.localdate()
    zero = Decimal("0")

    # Every figure below is computed by the database (SUM / GROUP BY), not by looping in Python.
    total_balance = Account.objects.filter(user=user).aggregate(
        total=Sum("balance", default=zero)
    )["total"]
    income_month = Income.objects.filter(
        user=user, date__year=today.year, date__month=today.month
    ).aggregate(total=Sum("amount", default=zero))["total"]

    # One grouped query: this month's spending per category.
    spent_by_category = {
        row["category"]: row["total"]
        for row in Expense.objects.filter(
            user=user, date__year=today.year, date__month=today.month
        ).values("category").annotate(total=Sum("amount"))
    }
    expenses_month = sum(spent_by_category.values(), zero)

    # Budget usage reuses the grouped result, so it needs no extra query per budget.
    budget_rows = []
    limit_sum = zero
    spent_sum = zero
    this_month = Budget.objects.filter(
        user=user, month=today.replace(day=1)
    ).select_related("category")
    for budget in this_month:
        spent = spent_by_category.get(budget.category_id, zero)
        limit_sum += budget.limit_amount
        spent_sum += spent
        percent = int(spent / budget.limit_amount * 100) if budget.limit_amount else 0
        budget_rows.append({
            "category": budget.category.name,
            "spent": money(spent),
            "limit": money(budget.limit_amount),
            "percent": percent,
            "bar": min(percent, 100),
        })

    # One grouped query: spending per month for the current year (drives the bar chart).
    per_month = {m: zero for m in range(1, 13)}
    yearly = (
        Expense.objects.filter(user=user, date__year=today.year)
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
    )
    for row in yearly:
        per_month[row["month"]] = row["total"]
    peak = max(per_month.values())
    chart = [
        {
            "label": calendar.month_abbr[m],
            "height": int(per_month[m] / peak * 100) if peak else 0,
            "amount": money(per_month[m]),
        }
        for m in range(1, 13)
    ]
    chart_axis = [compact_money(peak * Decimal(step) / 4) for step in (4, 3, 2, 1, 0)]

    recent = [
        {"title": e.title, "kind": "Expense", "amount": f"−{money(e.amount)}", "date": e.date, "income": False}
        for e in Expense.objects.filter(user=user).order_by("-date", "-id")[:5]
    ] + [
        {"title": i.source, "kind": "Income", "amount": f"+{money(i.amount)}", "date": i.date, "income": True}
        for i in Income.objects.filter(user=user).order_by("-date", "-id")[:5]
    ]
    recent.sort(key=lambda row: row["date"], reverse=True)

    return render(request, "dashboard.html", {
        "page": "dashboard",
        "total_balance": money(total_balance),
        "income_month": money(income_month),
        "expenses_month": money(expenses_month),
        "budget_remaining": money(limit_sum - spent_sum),
        "budget_rows": budget_rows,
        "recent": recent[:5],
        "chart": chart,
        "chart_axis": chart_axis,
        "chart_year": today.year,
    })


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "profile.html", {"page": "profile", "form": form})