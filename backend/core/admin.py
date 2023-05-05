from django.contrib import admin

from .models import Account, Transaction, FinancialGoal, Spending


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'current_money')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'amount', 'data')


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'label', 'finished', 'goal_money', 'current_money')


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'label', 'finished', 'goal_money', 'current_money', 'to_go_date')
