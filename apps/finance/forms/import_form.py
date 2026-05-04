from django import forms


class ImportTransactionForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")
