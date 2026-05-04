from django.contrib.auth import get_user_model
from apps.finance.models import Budget

User = get_user_model()


class BudgetRepository:
    def get_user_budgets(self, user: User, **kwargs):
        """Get user's budgets with optional filters."""
        return Budget.objects.filter(user=user)

    def get_active_budgets(self, user: User):
        """Get active budgets for user."""
        return Budget.objects.filter(user=user, is_active=True)
