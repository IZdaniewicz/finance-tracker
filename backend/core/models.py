from django.db import models


class Account(models.Model):
    class Meta:
        verbose_name_plural = "Accounts"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    user = models.CharField(default="user", max_length=20)
    current_money = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user}'


class Transaction(models.Model):
    class Meta:
        verbose_name_plural = "Transactions"
        app_label = "core"

    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)
    label = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.label} ({self.amount})'
