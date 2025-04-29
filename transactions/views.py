from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib import messages

from .forms import TransactionForm
from .models import Transaction

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transactions:list')
    template_name = 'transactions/add_transaction.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST, user = request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            user = request.user
            if transaction.transaction_type == 'Income':
                user.balance += transaction.amount
                transaction.save()
                user.save()
                return redirect('transactions:transactions_list')
            else:
                if (user.balance - transaction.amount) >= 0:
                    user.balance -= transaction.amount
                    transaction.save()
                    user.save()
                    return redirect('transactions:transactions_list')
                else:
                    messages.error(request, 'Insufficient funds')

        return render(request, 'transactions/add_transaction.html', {'form': form})


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    paginate_by = 10
    template_name = 'transactions/transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

@login_required
def transactions_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, user = request.user, id = transaction_id)
    transaction.delete()
    return redirect('transactions:transactions_list')