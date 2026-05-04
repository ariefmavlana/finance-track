from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class FinancialAccount(BaseModel):
    TYPE_BANK = "bank"
    TYPE_CASH = "cash"
    TYPE_CREDIT_CARD = "credit_card"
    TYPE_INVESTMENT = "investment"
    TYPE_LOAN = "loan"
    TYPE_E_WALLET = "e_wallet"

    ACCOUNT_TYPES = [
        (TYPE_BANK, "Bank Account"),
        (TYPE_CASH, "Cash"),
        (TYPE_CREDIT_CARD, "Credit Card"),
        (TYPE_INVESTMENT, "Investment"),
        (TYPE_LOAN, "Loan"),
        (TYPE_E_WALLET, "E-Wallet"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="financial_accounts"
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.CharField(max_length=3, default="IDR")
    initial_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    current_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    color = models.CharField(max_length=7, default="#3B82F6")
    icon = models.CharField(max_length=50, default="wallet")
    is_active = models.BooleanField(default=True)
    institution_name = models.CharField(max_length=100, blank=True)
    last_four_digits = models.CharField(max_length=4, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "finance_financial_account"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_account_type_display()})"