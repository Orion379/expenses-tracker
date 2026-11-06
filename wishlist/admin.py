from django.contrib import admin

from .models import WishlistItem


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("name", "target_price", "priority", "status", "user")
    list_filter = ("priority", "status")