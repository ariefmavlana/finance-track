from django import forms
from apps.finance.models import FinancialAccount


class AccountForm(forms.ModelForm):
    class Meta:
        model = FinancialAccount
        fields = ["name", "account_type", "currency", "initial_balance"]
