from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel
from .category import Category

User = get_user_model()


class Budget(BaseModel):
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"
    PERIOD_QUARTERLY = "quarterly"
    PERIOD_YEARLY = "yearly"
    PERIOD_CUSTOM = "custom"

    PERIODS = [
        (PERIOD_WEEKLY, "Weekly"),
        (PERIOD_MONTHLY, "Monthly"),
        (PERIOD_QUARTERLY, "Quarterly"),
        (PERIOD_YEARLY, "Yearly"),
        (PERIOD_CUSTOM, "Custom"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budgets"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    period = models.CharField(max_length=10, choices=PERIODS, default=PERIOD_MONTHLY)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    alert_at_percentage = models.PositiveSmallIntegerField(default=80)
    alert_sent = models.BooleanField(default=False)

    class Meta:
        db_table = "finance_budget"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} — {self.amount} {self.currency}/{self.period}"