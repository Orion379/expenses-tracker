from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import RecurringExpense


@login_required
def recurring_list(request):
    items = (
        RecurringExpense.objects.filter(user=request.user)
        .select_related("category", "account")
        .order_by("next_due_date")
    )
    return render(request, "recurring.html", {"recurring_expenses": items})