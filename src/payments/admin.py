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


class CityAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country']
    list_filter = ['country']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class StripeAcceptedCountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'country']
    list_filter = ['country']


class ExternalAccountAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'connect', 'country', 'account_holder_name',
        'account_number', 'created_on', 'is_verified'
    ]
    list_filter = ['is_active', 'is_verified', 'account_holder_type', 'country']
    search_fields = ['connect', 'account_holder_name', 'account_number']


admin.site.register(City, CityAdmin)
admin.site.register(StripeAcceptedCountry, StripeAcceptedCountryAdmin)
admin.site.register(Connect, ConnectAdmin)
admin.site.register(ExternalAccount, ExternalAccountAdmin)
admin.site.register(Currency, CurrencyAdmin)