from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm
from .models import Transaction

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('transactions:transactions_list')
    else:
        form = TransactionForm()

    return render(request, 'transactions/add_transaction.html', {'form': form})


def transactions_list(request):
    transactions = Transaction.objects.filter(user = request.user)
    return render(request, 'transactions/transactions_list.html', {'transactions': transactions})

def transactions_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, user = request.user, id = transaction_id)
    transaction.delete()
    return redirect('transactions:transactions_list')