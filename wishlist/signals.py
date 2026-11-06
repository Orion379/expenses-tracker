from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import WishlistItem


@receiver(pre_save, sender=WishlistItem)
def mark_purchased_when_expense_linked(sender, instance, **kwargs):
    if instance.expense_id:
        instance.status = WishlistItem.Status.PURCHASED