from src.portals.admins.models import Country, PaymentMethod
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            'pk',
            'name',
            'description',
            'is_active',
        )


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = (
            'pk',
            'name',
            'icon',
            'image',
            'country',
            'is_active',
        )
