from decimal import Decimal
from datetime import date
from typing import Optional

from django.db.models import Sum, Q
from django.contrib.auth import get_user_model

from apps.finance.models import Budget, Category, Transaction

User = get_user_model()


class BudgetService:
    def get_active_budgets_with_usage(self, user: User, ref_date: Optional[date] = None):
        """
        Kembalikan budget aktif beserta jumlah yang sudah dipakai.
        """
        ref_date = ref_date or date.today()
        budgets = Budget.objects.filter(
            user=user, is_active=True
        ).select_related("category")

        result = []
        for budget in budgets:
            spent = self._get_spent_amount(user, budget, ref_date)
            percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
            result.append({
                "budget": budget,
                "spent": spent,
                "remaining": max(budget.amount - spent, Decimal("0")),
                "percentage": round(percentage, 1),
                "is_over": spent > budget.amount,
            })
        return result

    def _get_spent_amount(
        self, user: User, budget: Budget, ref_date: date
    ) -> Decimal:
        """Hitung total pengeluaran untuk budget di periode aktif."""
        from apps.finance.utils.dates import get_period_dates
        start, end = get_period_dates(budget.period, ref_date)

        result = Transaction.objects.filter(
            user=user,
            category=budget.category,
            transaction_type=Transaction.TYPE_EXPENSE,
            date__gte=start,
            date__lte=end,
        ).aggregate(total=Sum("amount"))
        return result["total"] or Decimal("0")

    def check_and_alert(self, user: User, category: Category) -> None:
        """Cek apakah budget melebihi threshold dan kirim alert."""
        budgets = Budget.objects.filter(
            user=user, category=category, is_active=True, alert_sent=False
        )
        for budget in budgets:
            usage = self.get_active_budgets_with_usage(user)
            for item in usage:
                if item["budget"].pk == budget.pk:
                    if item["percentage"] >= budget.alert_at_percentage:
                        self._send_budget_alert(budget, item["percentage"])
                    break

    def _send_budget_alert(self, budget: Budget, percentage: float) -> None:
        from apps.finance.tasks import send_budget_alert
        send_budget_alert.delay(str(budget.pk), budget.user_id, percentage)
        budget.alert_sent = True
        budget.save(update_fields=["alert_sent"])