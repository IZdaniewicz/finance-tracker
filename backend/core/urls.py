from django.urls import path

from . import views
from .views import RegisterUserView

urlpatterns = [
    path("account/<int:account_id>", views.get_account_by_id),

    path("account", views.AccountAPIView.as_view()),
    path("transaction", views.TransactionAPIView.as_view()),

    path("transaction/<int:transaction_id>", views.get_transaction_by_id),
    path("transaction/day/<int:day>", views.get_all_transaction_by_day),
    path("transaction/month/<int:month>", views.get_all_transaction_by_month),
    path("account/transaction/<int:account_id>", views.get_all_transaction_by_account_id),
    path('register/', RegisterUserView.as_view(), name='register'),
    path("logout", views.LogoutView.as_view(), name="logout")
]
