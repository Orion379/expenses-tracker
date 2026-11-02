from django.db import models
from django.conf import settings
from accounts.models import Account

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    source = models.CharField(max_length=200, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.source} {self.amount} {self.account}"