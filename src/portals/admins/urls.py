from django.urls import path

from src.portals.admins.views import (
    DashboardView,
    UserListView, UserDetailView, UserUpdateView, UserPasswordResetView,
    TopUpListView, TopUpDetailView, TopUpInvoiceView,
    TransactionListView, TransactionDetailView, TransactionInvoiceView,
    WithdrawalListView, WithdrawalDetailView, WithdrawalInvoiceView,
    TicketListView, TicketDetailView,
    TicketStatusChangeView)

app_name = "admin-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

    path('topup/', TopUpListView.as_view(), name='topup-list'),
    path('topup/<int:pk>/', TopUpDetailView.as_view(), name='topup-detail'),
    path('topup/<int:pk>/invoice/', TopUpInvoiceView.as_view(), name='topup-invoice'),

    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/invoice/', TransactionInvoiceView.as_view(), name='transaction-invoice'),

    path('withdrawal/', WithdrawalListView.as_view(), name='withdrawal-list'),
    path('withdrawal/<int:pk>/', WithdrawalDetailView.as_view(), name='withdrawal-detail'),
    path('withdrawal/<int:pk>/invoice/', WithdrawalInvoiceView.as_view(), name='withdrawal-invoice'),

    path('ticket/', TicketListView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/<int:pk>/status/change/', TicketStatusChangeView.as_view(), name='ticket-status-change'),

]
