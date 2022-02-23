from django.urls import path
from .views import (
    DashboardView, WalletDetailView,
    TopUpListView, TopUpInvoiceView, TopUpDetailView, TopUpCreateView,
    TransactionListView, TransactionDetailView, TransactionInvoiceView, TransactionCreateView,
    WithdrawalListView, WithdrawalInvoiceView, WithdrawalDetailView
)

app_name = "customer-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),

    path('topup/', TopUpListView.as_view(), name='topup-list'),
    path('topup/1/', TopUpDetailView.as_view(), name='topup-detail'),
    path('topup/add/', TopUpCreateView.as_view(), name='topup-create'),
    path('topup/invoice/', TopUpInvoiceView.as_view(), name='topup-invoice'),

    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/1/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/add/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transaction/invoice/', TransactionInvoiceView.as_view(), name='transaction-invoice'),

    path('withdrawal/', WithdrawalListView.as_view(), name='withdrawal-list'),
    path('withdrawal/1/', WithdrawalDetailView.as_view(), name='withdrawal-detail'),
    path('withdrawal/invoice/', WithdrawalInvoiceView.as_view(), name='withdrawal-invoice'),

]
