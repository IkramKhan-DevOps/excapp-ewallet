import django_filters

from src.portals.admins.models import Country, PaymentMethod
from . import serializers
from rest_framework import viewsets, permissions


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [permissions.AllowAny]


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = serializers.PaymentMethodSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['country']

