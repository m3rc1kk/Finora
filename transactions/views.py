from django.shortcuts import render, redirect
from .forms import TransactionForm


def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('main:dashboard')
    else:
        form = TransactionForm()

    return render(request, 'transactions/add_transaction.html', {'form': form})
