from django.db import models
from django.conf import settings
from accounts.models import Account
from categories.models import Category
from recurring.models import RecurringExpense

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    recurring_expense = models.ForeignKey(RecurringExpense, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField()
    
    def __str__(self):
        return f"{self.title} {self.amount} {self.date}"
    
