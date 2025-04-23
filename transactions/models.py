from django.db import models
from django.conf import settings

from categories.models import Category


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transactions')
    transaction_type = models.CharField(
        max_length=7,
        choices=TRANSACTION_TYPES,
        blank=False,
        default='Expense',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='transactions', blank=False, null=True, default='Health',)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.date})"
