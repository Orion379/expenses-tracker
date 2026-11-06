from django.tasks import task

from .processing import process_due_recurring_expenses


@task
def process_recurring_expenses():
    return process_due_recurring_expenses()