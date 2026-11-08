def unread_notifications(request):
    """Makes the unread notification count available to the sidebar on every page."""
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    from notifications.models import Notification

    return {"unread_notifications": Notification.objects.filter(user=user, is_read=False).count()}