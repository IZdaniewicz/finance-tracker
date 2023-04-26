from django.urls import path

from . import views
urlpatterns = [
    path("account/<int:account_id>", views.GetAccountById),

    path("account", views.AccountAPIView.as_view()),
    path("transaction", views.TransactionAPIView.as_view()),

    path("transaction/<int:transaction_id>", views.GetTransactionById),
    path("transaction/day/<int:day>", views.GetAllTransactionByDay),
    path("transaction/month/<int:month>", views.GetAllTransactionByMonth),
    path("account/transaction/<int:account_id>", views.GetAllTransactionByAccountId),
]

