from django.urls import path
from .views import (

    stripe_config,
    create_checkout_session, CancelledView, SuccessView,
    create_checkout_session_280, create_checkout_session_40
)

app_name = 'payment-stripe'
urlpatterns = [

    path('config/', stripe_config, name='stripe-config'),
    path('create-checkout-session-280/', create_checkout_session_280, name='create_checkout_session_280'),  # new
    path('create-checkout-session-40/', create_checkout_session_40, name='create_checkout_session_40'),  # new
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),  # new
    path('success/', SuccessView.as_view(), name='success'),  # new
    path('cancelled/', CancelledView.as_view(), name='cancel'),  # new
]