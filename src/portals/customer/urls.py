from django.urls import path
from .views import (
    DashboardView, WalletDetailView
)

app_name = "customer-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),

]
