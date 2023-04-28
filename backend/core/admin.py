from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'current_money')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'amount', 'data')
