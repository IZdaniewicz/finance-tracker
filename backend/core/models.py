from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    class Meta:
        verbose_name_plural = "Accounts"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    current_money = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} account: {self.current_money}'


class Transaction(models.Model):
    class Meta:
        verbose_name_plural = "Transactions"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False)
    amount = models.FloatField(blank=False)
    data = models.DateTimeField(auto_now_add=True)
    label = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.label} ({self.amount})'


@receiver(post_save, sender=Transaction)
def process_transaction_init(sender, instance, **kwargs):
    transaction = instance
    transaction.account.current_money += transaction.amount
    transaction.account.save()
    try:
        if transaction.label is not None:
            if transaction.amount > 0.0:
                x = FinancialGoal.objects.get(label=transaction.label)
                x.current_money += transaction.amount
            else:
                x = Spending.objects.get(label=transaction.label)
                x.current_money -= transaction.amount
            if x.current_money > x.goal_money:
                x.current_money = x.goal_money
                x.finished = True
            x.save()
    except Spending.DoesNotExist:
        return
    except FinancialGoal.DoesNotExist:
        return


# post_save.connect(process_transaction_init, Transaction)


class FinancialGoal(models.Model):
    class Meta:
        verbose_name_plural = "Financial Goals"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(blank=False, max_length=100)
    label = models.CharField(blank=False, max_length=100, unique=True)
    finished = models.BooleanField(default=False)
    goal_money = models.FloatField()
    current_money = models.FloatField(default=0)

    def get_all_goal_transactions(self):
        try:
            return Transaction.objects.filter(label=self.label)
        except Transaction.DoesNotExist:
            return None


class Spending(models.Model):
    class Meta:
        verbose_name_plural = "Spendings"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(blank=False, max_length=100)
    label = models.CharField(blank=False, max_length=100, unique=True)
    finished = models.BooleanField(default=False)
    goal_money = models.FloatField()
    current_money = models.FloatField(default=0)
    to_go_date = models.DateTimeField('%Y-%m-%d')

    def get_all_goal_transactions(self):
        try:
            return Transaction.objects.filter(label=self.label)
        except Transaction.DoesNotExist:
            return None
