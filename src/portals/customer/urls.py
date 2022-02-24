from django.urls import path
from .views import (
    DashboardView, WalletDetailView,
    TopUpListView, TopUpInvoiceView, TopUpDetailView, TopUpCreateView,
    TransactionListView, TransactionDetailView, TransactionInvoiceView, TransactionCreateView,
    WithdrawalListView, WithdrawalInvoiceView, WithdrawalDetailView, WithdrawalCreateView
)

app_name = "customer-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),

    path('topup/', TopUpListView.as_view(), name='topup-list'),
    path('topup/add/', TopUpCreateView.as_view(), name='topup-create'),
    path('topup/<int:pk>/', TopUpDetailView.as_view(), name='topup-detail'),
    path('topup/<int:pk>/invoice/', TopUpInvoiceView.as_view(), name='topup-invoice'),

    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/add/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/invoice/', TransactionInvoiceView.as_view(), name='transaction-invoice'),

    path('withdrawal/', WithdrawalListView.as_view(), name='withdrawal-list'),
    path('withdrawal/add/', WithdrawalCreateView.as_view(), name='withdrawal-create'),
    path('withdrawal/<int:pk>/', WithdrawalDetailView.as_view(), name='withdrawal-detail'),
    path('withdrawal/<int:pk>/invoice/', WithdrawalInvoiceView.as_view(), name='withdrawal-invoice'),

]
