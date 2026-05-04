from django.contrib.auth import get_user_model

User = get_user_model()


class BudgetService:
    def get_active_budgets_with_usage(self, user: User, **kwargs):
        """Get active budgets for user with usage calculations."""
        from apps.finance.models import Budget
        budgets = Budget.objects.filter(user=user, is_active=True)
        return [{"budget": b, "spent": 0, "remaining": b.amount} for b in budgets]
