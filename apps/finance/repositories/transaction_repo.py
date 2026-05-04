from django.contrib.auth import get_user_model
from apps.finance.models import Transaction
from datetime import date
from typing import Optional

User = get_user_model()


class TransactionRepository:
    def get_user_transactions(self, user: User, **kwargs):
        """Get user's transactions with optional filters."""
        qs = Transaction.objects.filter(user=user)
        return qs

    def get_recent(self, user: User, limit: int = 10):
        """Get recent transactions for user."""
        return Transaction.objects.filter(user=user).order_by("-date")[:limit]

    def get_monthly_summary(self, user: User, year: int, month: int):
        """Get monthly summary for user."""
        return {
            "income": 0,
            "expense": 0,
            "net": 0,
        }

    def create(self, **kwargs) -> Transaction:
        """Create a new transaction."""
        return Transaction.objects.create(**kwargs)
