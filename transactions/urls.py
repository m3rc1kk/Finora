from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/<int:transaction_id>/', views.transactions_delete, name='transaction_delete'),
    path('', views.transactions_list, name='transactions_list'),
]