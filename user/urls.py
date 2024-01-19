from django.urls import path
from . import views
urlpatterns = [
    path("", views.Testing.as_view()),
    path("register/", views.UserService.as_view()),
    path("deposit/", views.DepositView.as_view()),
    path("withdraw/", views.WithdrawView.as_view()),
    path('api/transaction-history/<str:account_number>/', views.TransactionHistoryView.as_view(), name='transaction-history'),
    
]
