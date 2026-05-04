from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class Notification(TimeStampedModel):
    TYPE_BUDGET_ALERT = "budget_alert"
    TYPE_LARGE_TRANSACTION = "large_transaction"
    TYPE_RECURRING = "recurring"
    TYPE_SYSTEM = "system"

    TYPES = [
        (TYPE_BUDGET_ALERT, "Budget Alert"),
        (TYPE_LARGE_TRANSACTION, "Large Transaction"),
        (TYPE_RECURRING, "Recurring Transaction"),
        (TYPE_SYSTEM, "System"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.notification_type}: {self.title} ({self.user.email})"