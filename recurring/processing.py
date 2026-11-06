import calendar
import datetime
import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from expenses.models import Expense
from .models import RecurringExpense

logger = logging.getLogger(__name__)


def add_months(date, months):
    month_index = date.month - 1 + months
    year = date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


def next_due_date(current, frequency):
    if frequency == RecurringExpense.Frequency.WEEKLY:
        return current + datetime.timedelta(days=7)
    if frequency == RecurringExpense.Frequency.MONTHLY:
        return add_months(current, 1)
    return add_months(current, 12)


def process_due_recurring_expenses(today=None):
    today = today or timezone.localdate()
    created = 0
    for recurring in RecurringExpense.objects.filter(next_due_date__lte=today):
        count = 0
        try:
            with transaction.atomic():
                while recurring.next_due_date <= today:
                    Expense.objects.create(
                        user=recurring.user,
                        category=recurring.category,
                        account=recurring.account,
                        recurring_expense=recurring,
                        title=recurring.title,
                        amount=recurring.amount,
                        date=recurring.next_due_date,
                        note="Created automatically from a recurring expense.",
                    )
                    count += 1
                    recurring.next_due_date = next_due_date(
                        recurring.next_due_date, recurring.frequency
                    )
                recurring.save(update_fields=["next_due_date"])
        except ValidationError as error:
            logger.warning("Skipped recurring expense %s: %s", recurring.pk, error)
            continue
        created += count
    return created