from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField, FloatField

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = (
            'user',
            'current_money'
        )

    def create(self, validated_data):
        user = validated_data.pop('user')
        account = models.Account.objects.create(user=user, **validated_data)
        return account


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
