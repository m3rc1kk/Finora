from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
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

    expenses = (
        Transaction.objects.filter(
            user = user,
            transaction_type = 'Expense',
            date__month = current_month,
            date__year = current_year,
            ).values('category__name', 'category__color').annotate(total=Sum('amount')).order_by('-total')
    )

    categories = []
    amounts = {}
    category_colors = {}
    categories_data = []

    for i, item in enumerate(expenses):
        category = item['category__name']
        categories.append(category)
        amounts[category] = float(item['total'])
        category_colors[category] = item['category__color']
        categories_data.append((category, item['category__color'], float(item['total'])))

    labels = []
    income_data = []
    expense_data = []

    for i in range(12):
        month = (current_month - i - 1) % 12 + 1
        year = current_year if current_month - i - 1 >= 0 else current_year - 1
        labels.insert(0, month_name[month])

        income = Transaction.objects.filter(
            user=user,
            transaction_type='Income',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense = Transaction.objects.filter(
            user=user,
            transaction_type='Expense',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        income_data.insert(0, float(income))
        expense_data.insert(0, float(expense))

    return render(request, 'main/dashboard.html', {
        'current_month_income': income,
        'current_month_expenses': expense,
        'current_month_difference': income - expense,
        'current_month': month_name[current_month],
        'transactions': transactions,
        'max_balance': max_balance,
        'month_comparison': month_comparison,
        'categories_json': json.dumps(categories, cls=DjangoJSONEncoder),
        'amounts_json': json.dumps(list(amounts.values()), cls=DjangoJSONEncoder),
        'colors_json': json.dumps(list(category_colors.values()), cls=DjangoJSONEncoder),
        'categories_data': categories_data,
        'labels': json.dumps(labels, cls=DjangoJSONEncoder),
        'income_data': json.dumps(income_data, cls=DjangoJSONEncoder),
        'expense_data': json.dumps(expense_data, cls=DjangoJSONEncoder)
    })