from decimal import Decimal
from datetime import date
from typing import Optional

from django.db.models import Sum, Q, Count
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, Category

User = get_user_model()


class ReportService:
    def get_summary(
        self,
        user: User,
        start_date: date,
        end_date: date,
    ) -> dict:
        """Summary: total income, expense, net, dan per-category."""
        qs = Transaction.objects.filter(
            user=user, date__gte=start_date, date__lte=end_date
        )

        totals = qs.aggregate(
            total_income=Sum("amount", filter=Q(transaction_type="income")),
            total_expense=Sum("amount", filter=Q(transaction_type="expense")),
        )
        total_income = totals["total_income"] or Decimal("0")
        total_expense = totals["total_expense"] or Decimal("0")

        by_category = (
            qs.filter(transaction_type="expense")
            .values("category__name", "category__color", "category__icon")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )

        monthly_trend = []
        from apps.finance.utils.dates import months_between
        for year, month in months_between(start_date, end_date):
            month_qs = qs.filter(date__year=year, date__month=month)
            month_totals = month_qs.aggregate(
                income=Sum("amount", filter=Q(transaction_type="income")),
                expense=Sum("amount", filter=Q(transaction_type="expense")),
            )
            monthly_trend.append({
                "year": year,
                "month": month,
                "income": month_totals["income"] or 0,
                "expense": month_totals["expense"] or 0,
            })

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net": total_income - total_expense,
            "by_category": list(by_category),
            "monthly_trend": monthly_trend,
        }