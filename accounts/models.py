from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    account_type = models.CharField(max_length=30)

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.name
