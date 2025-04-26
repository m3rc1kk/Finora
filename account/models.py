from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.urls import reverse


def user_directory_path(instance, filename):
    return f'{instance.username}/profile_avatars/{filename}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def get_monthly_income(self, month, year):
        return self.user_transactions.filter(
            transaction_type = 'Income',
            date__month = month,
            date__year = year
        ).aggregate(total=Sum('amount'))['total'] or 0

    def get_monthly_expense(self, month, year):
        return self.user_transactions.filter(
            transaction_type = 'Expense',
            date__month = month,
            date__year = year
        ).aggregate(total=Sum('amount'))['total'] or 0

    def get_personal_best(self):
        transactions = self.user_transactions.all().order_by('date')

        current_balance = 0
        max_balance = 0

        for transaction in transactions:
            if transaction.transaction_type == 'Income':
                current_balance += transaction.amount
            else:
                current_balance -= transaction.amount
            if current_balance > max_balance:
                max_balance = current_balance

        return max_balance


    def get_monthly_comparison(self):
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        current_income = self.get_monthly_income(current_month, current_year)
        current_expense = self.get_monthly_expense(current_month, current_year)
        current_difference = current_income - current_expense

        prev_month_date = current_date - timedelta(days=current_date.day)
        prev_month = prev_month_date.month
        prev_year = prev_month_date.year

        prev_income = self.get_monthly_income(prev_month, prev_year)
        prev_expense = self.get_monthly_expense(prev_month, prev_year)
        prev_difference = prev_income - prev_expense

        if prev_difference != 0:
            percent_diff = ((current_difference - prev_difference) / abs(prev_difference)) * 100
        else:
            percent_diff = 0

        if current_difference > prev_difference:
            comparison = 'better'
        elif current_difference < prev_difference:
            comparison = 'worse'
        else:
            comparison = 'same'

        if prev_income != 0:
            percent_income = ((current_income - prev_income) / abs(prev_income)) * 100
        else:
            percent_income = 0

        if current_income > prev_income:
            comparison_income = 'better'
        elif current_income < prev_income:
            comparison_income = 'worse'
        else:
            comparison_income = 'same'

        if prev_expense != 0:
            percent_expense = ((current_expense - prev_expense) / abs(prev_expense)) * 100
        else:
            percent_expense = 0

        if current_expense > prev_expense:
            comparison_expense = 'better'
        elif current_expense < prev_expense:
            comparison_expense = 'worse'
        else:
            comparison_expense = 'same'


        return {
            'percent_diff': abs(round(percent_diff)),
            'comparison': comparison,
            'comparison_income': comparison_income,
            'percent_income': abs(round(percent_income)),
            'percent_expense': abs(round(percent_expense)),
            'comparison_expense': comparison_expense,
        }


    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args = [self.id])

