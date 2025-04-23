from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_type', 'amount', 'date', 'category')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

