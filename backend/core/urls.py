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
    path('goals/', views.FinancialGoalListCreateView.as_view(), name='goal-list-create'),
    path('goals/<int:pk>/', views.FinancialGoalRetrieveUpdateDestroyView.as_view(), name='goal-detail'),
    path('goals/<int:pk>/transactions/', views.FinancialGoalRetrieveUpdateDestroyView.as_view(),
         name='goal-transactions'),
    path('spendings/', views.SpendingListCreateView.as_view(), name='spending-list-create'),
    path('spendings/<int:pk>/', views.SpendingListRetrieveUpdateDestroyView.as_view(), name='spending-detail'),
    path('spendings/<int:pk>/transactions/', views.SpendingListRetrieveUpdateDestroyView.as_view(),
         name='spending-transactions'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path("logout", views.LogoutView.as_view(), name="logout")
]
