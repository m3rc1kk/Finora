from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'date' )

