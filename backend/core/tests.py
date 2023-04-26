from rest_framework.test import APITestCase
from rest_framework import status
from backend.core.models import Account


class AccountTests(APITestCase):
    def setUp(self):
        self.account = Account.objects.create(user='test_user', current_money=100.0)

    def test_get_all_accounts(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.account.user, str(response.data))

    # def test_get_account_by_id(self):
    #     # Send a GET request to fetch the account by ID
    #     response = self.client.get('/accounts/{}/'.format(self.account.id))
    #     # Check that the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Check that the response contains the sample account we created
    #     self.assertEqual(response.data['user'], self.account.user)
    #     self.assertEqual(response.data['current_money'], self.account.current_money)

    def test_create_account(self):
        account_data = {
            "user": "new_user",
            "current_money": 50.0
        }
        response = self.client.post('/', account_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(response.data['user'], account_data['user'])
        self.assertEqual(response.data['current_money'], account_data['current_money'])
