from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.validators import MinValueValidator
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
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    date = models.DateField()
    note = models.TextField(blank=True)
    
    def clean(self):
        super().clean()
        if self.user_id and self.account_id:
            if self.account.user_id != self.user_id:
                raise ValidationError({"account": "This account does not belong to the selected user"})
            
        if self.user_id and self.category_id:
            if self.category.user_id != self.user_id:
                raise ValidationError({"category": "This category does not belong to the selected user"})
            
        if self.user_id and self.recurring_expense_id:
            if self.recurring_expense.user_id != self.user_id:
                raise ValidationError({"recurring_expense": "This recurring expense does not belong to the selected user"})
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
            
    def __str__(self):
        return f"{self.title} {self.amount: .2f} {self.date}"
    
