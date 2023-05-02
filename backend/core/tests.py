from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Account, Transaction


class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('account')
        self.account = Account(user='essa', current_money=200.0)
        self.account.save()

    def test_create_account(self):
        data = {"user": "essa", "current_money": 200}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account(self):
        url = reverse('account-detail', kwargs={'account_id': self.account.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_accounts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransactionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('transaction')
        self.account = Account(user='essa', current_money=200.0)
        self.account.save()
        self.transaction = Transaction(account_id=self.account.id, amount=200.0)
        self.transaction.save()

    def test_create_transaction(self):
        data = {
            "account_id": self.account.id,
            "amount": 99,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction(self):
        url = reverse('transaction-detail', kwargs={'transaction_id': self.transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transactions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
