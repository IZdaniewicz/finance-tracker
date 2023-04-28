from rest_framework import serializers
from rest_framework.fields import CharField, FloatField

from . import models


class AccountSerializer(serializers.ModelSerializer):
    user = CharField(required=True)
    current_money = FloatField(required=True)

    class Meta:
        model = models.Account
        fields = (
            'user',
            'current_money'
        )


class TransactionSerializer(serializers.ModelSerializer):
    account_id = CharField(required=False)
    amount = FloatField(required=True)
    data = CharField(required=False)
    label = CharField(required=False, allow_null=True, allow_blank=True)
    description = CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = models.Transaction
        fields = (
            'account_id',
            'amount',
            'data',
            'label',
            'description'
        )
