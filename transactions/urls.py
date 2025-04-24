from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    path('add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('delete/<int:transaction_id>/', views.transactions_delete, name='transaction_delete'),
    path('', views.TransactionsListView.as_view(), name='transactions_list'),
]