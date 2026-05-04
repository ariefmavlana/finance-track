from decimal import Decimal
from typing import Optional
from datetime import date

from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, FinancialAccount, Category

User = get_user_model()


class TransactionService:
    def __init__(self):
        pass

    @db_transaction.atomic
    def create_transaction(
        self,
        user: User,
        account: FinancialAccount,
        category: Optional[Category],
        transaction_type: str,
        amount: Decimal,
        date: date,
        description: str,
        **kwargs,
    ) -> Transaction:
        """Buat transaksi baru dan update saldo akun."""
        txn = Transaction.objects.create(
            user=user,
            account=account,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            currency=account.currency,
            date=date,
            description=description,
            **kwargs,
        )
        return txn
