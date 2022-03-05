from django.urls import path, include
from rest_framework import routers
from src.api.views import CountryViewSet, PaymentMethodViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'country', CountryViewSet)
router.register(r'paymentmethod', PaymentMethodViewSet)

app_name = "api"
urlpatterns = (
    path('', include(router.urls)),
)