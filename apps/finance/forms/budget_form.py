from django import forms
from apps.finance.models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["name", "category", "amount", "currency", "period", "start_date", "end_date"]
