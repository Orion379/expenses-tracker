from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from accounts.models import Account

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    source = models.CharField(max_length=200, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    date = models.DateField()
    
    def clean(self):
        super().clean()
        
        if self.user_id and self.account_id:
            if self.account.user_id != self.user_id:
                raise ValidationError({"account": "The selected account does not belong to this user"})
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.source} {self.amount: .2f} {self.account}"