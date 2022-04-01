from django.contrib import admin
from .models import (
    StripeAcceptedCountry, Connect, City, Currency, ExternalAccount
)


class ConnectAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'user', 'connect_id', 'first_name', 'last_name', 'email', 'phone',
        'country', 'city', 'business_type', 'is_active', 'created_on'
    ]
    list_filter = ['is_active']
    search_fields = ['user', 'connect_id', 'first_name', 'last_name', 'email', 'phone']


class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'account_type', 'business_type', 'email', 'is_active', 'created_on']
    list_filter = ['is_active']


class CityAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country']
    list_filter = ['country']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class StripeAcceptedCountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'country']
    list_filter = ['country']


class StripePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'is_active', 'created_on']
    list_filter = ['is_active']
