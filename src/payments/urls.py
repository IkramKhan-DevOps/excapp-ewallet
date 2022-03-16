from django.urls import path
from .views import (

    stripe_config,
    create_checkout_session, CancelledView, SuccessView, stripe_webhook,
    StripeAuthorizeView, StripeAuthorizeCallbackView)

app_name = 'payment-stripe'
urlpatterns = [

    path('config/', stripe_config, name='stripe-config'),
    path('create-checkout-session/<int:pk>/', create_checkout_session, name='stripe-balance-load'),  # new
    path('success/', SuccessView.as_view(), name='success'),  # new
    path('cancelled/', CancelledView.as_view(), name='cancel'),  # new
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('authorize/', StripeAuthorizeView.as_view(), name='authorize'),
    path('users/oauth/callback/', StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
]
