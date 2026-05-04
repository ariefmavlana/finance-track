from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel
from .account import FinancialAccount
from .category import Category

User = get_user_model()


class RecurringTransaction(BaseModel):
    FREQ_DAILY = "daily"
    FREQ_WEEKLY = "weekly"
    FREQ_BIWEEKLY = "biweekly"
    FREQ_MONTHLY = "monthly"
    FREQ_QUARTERLY = "quarterly"
    FREQ_YEARLY = "yearly"

    FREQUENCIES = [
        (FREQ_DAILY, "Daily"),
        (FREQ_WEEKLY, "Weekly"),
        (FREQ_BIWEEKLY, "Bi-weekly"),
        (FREQ_MONTHLY, "Monthly"),
        (FREQ_QUARTERLY, "Quarterly"),
        (FREQ_YEARLY, "Yearly"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="recurring_transactions"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=[("income", "Income"), ("expense", "Expense")],
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    frequency = models.CharField(max_length=10, choices=FREQUENCIES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "finance_recurring_transaction"
        ordering = ["next_due_date"]

    def __str__(self) -> str:
        return f"{self.description} ({self.frequency})"

    def advance_next_due_date(self):
        """Maju ke tanggal berikutnya sesuai frekuensi."""
        from dateutil.relativedelta import relativedelta
        import datetime

        freq_map = {
            self.FREQ_DAILY: datetime.timedelta(days=1),
            self.FREQ_WEEKLY: datetime.timedelta(weeks=1),
            self.FREQ_BIWEEKLY: datetime.timedelta(weeks=2),
            self.FREQ_MONTHLY: relativedelta(months=1),
            self.FREQ_QUARTERLY: relativedelta(months=3),
            self.FREQ_YEARLY: relativedelta(years=1),
        }
        delta = freq_map.get(self.frequency)
        if delta:
            self.next_due_date = self.next_due_date + delta
            self.save(update_fields=["next_due_date"])