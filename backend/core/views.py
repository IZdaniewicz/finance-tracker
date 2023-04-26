from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import views, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountAPIView(views.APIView):
    serializer_class = AccountSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        accounts = Account.objects.all()
        if len(accounts) < 1:
            return JsonResponse({'error': f'No accounts in database.'}, status=404)
        serializer = AccountSerializer(accounts, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = AccountSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


def GetAccountById(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        data = {
            'user': account.user,
            'current_money': account.current_money,
        }
        return JsonResponse(data, safe=False)

    except Account.DoesNotExist:
        return JsonResponse({'error': f'Account with id={account_id} does not exist.'}, status=404)


class TransactionAPIView(views.APIView):
    serializer_class = TransactionSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        transactions = Transaction.objects.all()
        if len(transactions) < 1:
            return JsonResponse({'error': f'No transactions in database.'}, status=404)
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = TransactionSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Json decoding error"}, status=400)

    def put(self, request):
        try:
            data = JSONParser().parse(request)
            transaction_id = data['id']
            transaction = Transaction.objects.get(pk=transaction_id)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        try:
            data = JSONParser().parse(request)
            transaction_id = data['id']
            transaction = Transaction.objects.get(pk=transaction_id)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Transaction.DoesNotExist:
            return JsonResponse({'error': f'Transaction with id={transaction_id} does not exist.'}, status=404)


def GetTransactionById(request, transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
        data = {
            'account_id': transaction.account.id,
            'amount': transaction.amount,
            'date': transaction.data,
            'description': transaction.description,
            'label': transaction.label,
        }
        return JsonResponse(data, safe=False)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': f'Transaction with id={transaction_id} does not exist.'}, status=404)


def GetAllTransactionByAccountId(request, account_id):
    transactions = Transaction.objects.filter(account_id=account_id)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for account_id={account_id} does not exist.'}, status=404)
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


def GetAllTransactionByDay(request, day):
    transactions = Transaction.objects.filter(data__month=day)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for day={day} does not exist.'}, status=404)
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


def GetAllTransactionByMonth(request, month):
    transactions = Transaction.objects.filter(data__month=month)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for month={month} does not exist.'}, status=404)

    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)
