from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from config.crud import OwnedListCreateView
from .models import Notification


class NotificationPage(OwnedListCreateView):
    model = Notification
    form_class = None
    template_name = "notifications.html"
    page = "notifications"
    singular = "notification"
    context_name = "notifications"
    order_by = ("-created_at",)


@login_required
@require_POST
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect("notifications:list")


@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("notifications:list")