from django.core.management.base import BaseCommand

from recurring.processing import process_due_recurring_expenses


class Command(BaseCommand):
    help = "Create expenses for due recurring expenses and advance their due dates."

    def handle(self, *args, **options):
        created = process_due_recurring_expenses()
        self.stdout.write(self.style.SUCCESS(f"Created {created} expense(s)."))