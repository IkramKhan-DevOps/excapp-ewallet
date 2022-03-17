from django.urls import path
from .views import (
    DashboardView, WalletDetailView, WalletGenerateQRCodeView,
    TopUpListView, TopUpInvoiceView, TopUpDetailView, TopUpCreateView,
    TransactionListView, TransactionDetailView, TransactionInvoiceView, TransactionCreateView,
    WithdrawalListView, WithdrawalInvoiceView, WithdrawalDetailView, WithdrawalCreateView,
    UserSanctionsUpdateView,
    TicketListView, TicketCreateView, TicketDetailView,
    PaymentMethodView
)

app_name = "customer-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path('wallet/<int:pk>/generate/qr-code/', WalletGenerateQRCodeView.as_view(), name='generate-qr-code'),
    path('user/sanctions/change/', UserSanctionsUpdateView.as_view(), name='user-sanctions-change'),

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

    path('ticket/', TicketListView.as_view(), name='ticket-list'),
    path('ticket/add/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    path('payment-methods/', PaymentMethodView.as_view(), name='payment-methods'),
]
