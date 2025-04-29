from django import forms
from .models import Transaction
from django.db.models import Q
from categories.models import Category

class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['category'].queryset = Category.objects.filter(
                Q(user=None) | Q(user=self.user)
            )

    class Meta:
        model = Transaction
        fields = ('transaction_type', 'amount', 'date', 'category')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
