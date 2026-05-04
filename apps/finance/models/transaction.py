from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel
from .account import FinancialAccount
from .category import Category

User = get_user_model()


class Tag(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#9CA3AF")

    class Meta:
        db_table = "finance_tag"
        unique_together = [("user", "name")]

    def __str__(self) -> str:
        return self.name


class Transaction(BaseModel):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_TRANSFER = "transfer"

    TRANSACTION_TYPES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
        (TYPE_TRANSFER, "Transfer"),
    ]

    STATUS_PENDING = "pending"
    STATUS_CLEARED = "cleared"
    STATUS_RECONCILED = "reconciled"

    STATUSES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CLEARED, "Cleared"),
        (STATUS_RECONCILED, "Reconciled"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="transactions"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="transactions")
    transfer_to_account = models.ForeignKey(
        FinancialAccount, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="incoming_transfers"
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(max_length=3)
    amount_in_base_currency = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=6, null=True, blank=True
    )

    date = models.DateField(db_index=True)
    description = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    payee = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=15, choices=STATUSES, default=STATUS_CLEARED)
    reference_number = models.CharField(max_length=100, blank=True)
    receipt_image = models.ImageField(
        upload_to="receipts/%Y/%m/", blank=True, null=True
    )
    is_recurring_instance = models.BooleanField(default=False)
    recurring_transaction = models.ForeignKey(
        "finance.RecurringTransaction", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="instances"
    )

    class Meta:
        db_table = "finance_transaction"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category"]),
            models.Index(fields=["user", "transaction_type"]),
            models.Index(fields=["account", "date"]),
            models.Index(
                fields=["user", "deleted_at"],
                name="active_transactions_idx",
                condition=models.Q(deleted_at__isnull=True),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.description} — {self.amount} {self.currency} ({self.date})"

    @property
    def is_expense(self) -> bool:
        return self.transaction_type == self.TYPE_EXPENSE

    @property
    def is_income(self) -> bool:
        return self.transaction_type == self.TYPE_INCOME