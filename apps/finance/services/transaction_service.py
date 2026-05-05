from decimal import Decimal
from typing import Optional
from datetime import date

from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, FinancialAccount, Category, RecurringTransaction
from apps.finance.repositories.transaction_repo import TransactionRepository

User = get_user_model()


class TransactionService:
    def __init__(self, repo: Optional[TransactionRepository] = None):
        self.repo = repo or TransactionRepository()

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
        txn = self.repo.create(
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
        self._update_account_balance(account, txn)
        self._check_budget_alerts(user, txn)
        return txn

    @db_transaction.atomic
    def update_transaction(self, txn: Transaction, **fields) -> Transaction:
        """Update transaksi, balik dulu dampak saldo lama."""
        old_amount = txn.amount
        old_type = txn.transaction_type
        old_account = txn.account

        updated = self.repo.update(txn, **fields)

        # Balik dampak lama
        self._reverse_account_balance(old_account, old_amount, old_type)
        # Terapkan dampak baru
        self._update_account_balance(updated.account, updated)
        return updated

    @db_transaction.atomic
    def delete_transaction(self, txn: Transaction) -> None:
        """Soft-delete dan balik saldo akun."""
        self._reverse_account_balance(txn.account, txn.amount, txn.transaction_type)
        txn.delete()

    @db_transaction.atomic
    def create_from_recurring(
        self, recurring: RecurringTransaction, date: date
    ) -> Transaction:
        """Buat transaksi dari template recurring."""
        return self.create_transaction(
            user=recurring.user,
            account=recurring.account,
            category=recurring.category,
            transaction_type=recurring.transaction_type,
            amount=recurring.amount,
            date=date,
            description=recurring.description,
            is_recurring_instance=True,
            recurring_transaction=recurring,
        )

    def _update_account_balance(
        self, account: FinancialAccount, txn: Transaction
    ) -> None:
        if txn.transaction_type == Transaction.TYPE_INCOME:
            account.current_balance += txn.amount
        elif txn.transaction_type == Transaction.TYPE_EXPENSE:
            account.current_balance -= txn.amount
        elif txn.transaction_type == Transaction.TYPE_TRANSFER and txn.transfer_to_account:
            account.current_balance -= txn.amount
            txn.transfer_to_account.current_balance += txn.amount
            txn.transfer_to_account.save(update_fields=["current_balance"])
        account.save(update_fields=["current_balance"])

    def _reverse_account_balance(
        self, account: FinancialAccount, amount: Decimal, txn_type: str
    ) -> None:
        if txn_type == Transaction.TYPE_INCOME:
            account.current_balance -= amount
        elif txn_type == Transaction.TYPE_EXPENSE:
            account.current_balance += amount
        account.save(update_fields=["current_balance"])

    def _check_budget_alerts(self, user: User, txn: Transaction) -> None:
        if txn.transaction_type != Transaction.TYPE_EXPENSE or not txn.category:
            return
        from apps.finance.services.budget_service import BudgetService
        BudgetService().check_and_alert(user, txn.category)