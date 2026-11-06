from django.contrib import admin

from .models import RecurringExpense


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "frequency", "next_due_date", "user")
    list_filter = ("frequency",)