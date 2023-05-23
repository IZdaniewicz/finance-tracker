from json import JSONDecodeError

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import views, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, Transaction, FinancialGoal, Spending
from .serializers import AccountSerializer, TransactionSerializer, UserSerializer, FinancialGoalSerializer, \
    SpendingSerializer


class AccountAPIView(views.APIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

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
        data = JSONParser().parse(request)
        serializer = AccountSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, status=400)


def get_account_by_id(request, account_id):
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


def get_transaction_by_id(request, transaction_id):
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


def get_all_transaction_by_account_id(request, account_id):
    transactions = Transaction.objects.filter(account_id=account_id)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for account_id={account_id} does not exist.'}, status=404)
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_all_transaction_by_day(request, day):
    transactions = Transaction.objects.filter(data__month=day)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for day={day} does not exist.'}, status=404)
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_all_transaction_by_month(request, month):
    transactions = Transaction.objects.filter(data__month=month)
    if len(transactions) < 1:
        return JsonResponse({'error': f'Transactions for month={month} does not exist.'}, status=404)

    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        request.session.flush()
        return Response({"detail": "Logged out successfully."})


class RegisterUserView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            hashed_password = make_password(password)
            user = serializer.save(password=hashed_password)
            account_serializer = AccountSerializer(
                data={'user': user.id, 'current_money': request.data.get('current_money', 0)})
            if account_serializer.is_valid():
                account_serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinancialGoalListCreateView(generics.ListCreateAPIView):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinancialGoalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        goal = self.get_object()
        transactions = goal.get_all_goal_transactions()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, *args, **kwargs):
        goal = self.get_object()
        serializer = self.serializer_class(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpendingListCreateView(generics.ListCreateAPIView):
    queryset = Spending.objects.all()
    serializer_class = SpendingSerializer
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpendingListRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        goal = self.get_object()
        transactions = goal.get_all_goal_transactions()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, *args, **kwargs):
        goal = self.get_object()
        serializer = self.serializer_class(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        goal = self.get_object()
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
