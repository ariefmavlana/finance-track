from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationService:
    @staticmethod
    def create_notification(
        user: User,
        notification_type: str,
        title: str,
        message: str,
        url: str = "",
    ) -> Notification:
        """Create a notification for a user."""
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            url=url,
        )

    @staticmethod
    def mark_as_read(user: User, notification_id: int) -> bool:
        """Mark a notification as read."""
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_as_read(user: User) -> int:
        """Mark all notifications as read for a user."""
        count, _ = Notification.objects.filter(
            user=user, is_read=False
        ).update(is_read=True), None
        return count
