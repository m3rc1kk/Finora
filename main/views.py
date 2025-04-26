from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from calendar import month_name

from transactions.models import Transaction


def welcome(request):
    return render(request, 'main/welcome.html', {})
@login_required
def dashboard(request):
    user = request.user
    current_month = datetime.now().month
    current_year = datetime.now().year
    income = user.get_monthly_income(current_month, current_year)
    expense = user.get_monthly_expense(current_month, current_year)
    transactions = Transaction.objects.filter(user = user)[:6]
    max_balance = user.get_personal_best()
    month_comparison = user.get_monthly_comparison()

    return render(request, 'main/dashboard.html', {
        'current_month_income': income,
        'current_month_expenses': expense,
        'current_month_difference': income - expense,
        'current_month': month_name[current_month],
        'transactions': transactions,
        'max_balance': max_balance,
        'month_comparison': month_comparison,})