from django import forms
from apps.finance.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account", "category", "transaction_type", "amount", "date", "description", "notes"]


class ImportForm(forms.Form):
    file = forms.FileField()
