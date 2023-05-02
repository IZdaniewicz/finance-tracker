from django.urls import path

from . import views

urlpatterns = [

    path("account", views.AccountAPIView.as_view(), name='account'),
    path("account/<int:account_id>", views.GetAccountById, name='account-detail'),
    path("transaction", views.TransactionAPIView.as_view(), name='transaction'),
    path("transaction/<int:transaction_id>", views.GetTransactionById, name='transaction-detail'),

    path("transaction/day/<int:day>", views.GetAllTransactionByDay),
    path("transaction/month/<int:month>", views.GetAllTransactionByMonth),
    path("account/transaction/<int:account_id>", views.GetAllTransactionByAccountId),
]
