from django.urls import path

from src.portals.admins.views import (
    DashboardView,
    UserListView,
    TopUpListView, TopUpDetailView, TopUpInvoiceView,
    TransactionListView, TransactionDetailView, TransactionInvoiceView,
    WithdrawalListView, WithdrawalDetailView, WithdrawalInvoiceView
)

app_name = "admin-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user-list'),

    path('topup/', TopUpListView.as_view(), name='topup-list'),
    path('topup/<int:pk>/', TopUpDetailView.as_view(), name='topup-detail'),
    path('topup/<int:pk>/invoice/', TopUpInvoiceView.as_view(), name='topup-invoice'),

    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/invoice/', TransactionInvoiceView.as_view(), name='transaction-invoice'),

    path('withdrawal/', WithdrawalListView.as_view(), name='withdrawal-list'),
    path('withdrawal/<int:pk>/', WithdrawalDetailView.as_view(), name='withdrawal-detail'),
    path('withdrawal/<int:pk>/invoice/', WithdrawalInvoiceView.as_view(), name='withdrawal-invoice'),

]
