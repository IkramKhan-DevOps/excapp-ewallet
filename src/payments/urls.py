from django.urls import path
from .views import (
    stripe_config, create_checkout_session, CancelledView, SuccessView, stripe_webhook,
    ConnectCreateView, ConnectUpdateView, ConnectDetailView, ConnectDeleteView,
    ExternalAccountListView, ExternalAccountUpdateView, ExternalAccountDeleteView, ExternalAccountCreateView,
    ConnectVerifyView, ExternalAccountVerifyView)

app_name = 'payment-stripe'

urlpatterns = [
    path('connect/', ConnectDetailView.as_view(), name='connect'),
    path('connect/create/', ConnectCreateView.as_view(), name='connect-create'),
    path('connect/change/', ConnectUpdateView.as_view(), name='connect-update'),
    path('connect/delete/', ConnectDeleteView.as_view(), name='connect-delete'),

    path(
        'connect/external-account/', ExternalAccountListView.as_view(),
        name='connect-external-account'
    ),
    path(
        'connect/external-account/<int:pk>/change/', ExternalAccountUpdateView.as_view(),
        name='connect-external-account-change'
    ),
    path(
        'connect/external-account/create/', ExternalAccountCreateView.as_view(),
        name='connect-external-account-create'
    ),
    path(
        'connect/external-account/<int:pk>/delete/', ExternalAccountDeleteView.as_view(),
        name='connect-external-account-delete'
    ),

    path('connect/verify/', ConnectVerifyView.as_view(), name='connect-verify'),
    path(
        'connect/external-account/<int:pk>/verify/', ExternalAccountVerifyView.as_view(),
        name='connect-external-account-verify'
    )
]

urlpatterns += [
    path('config/', stripe_config, name='stripe-config'),
    path('create-checkout-session/<int:pk>/', create_checkout_session, name='stripe-balance-load'),  # new
    path('success/', SuccessView.as_view(), name='success'),  # new
    path('cancelled/', CancelledView.as_view(), name='cancel'),  # new
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
