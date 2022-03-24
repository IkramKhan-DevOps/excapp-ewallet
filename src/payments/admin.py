from django.contrib import admin
from .models import StripeCustomer, StripeAccount, StripeAcceptedCountry, StripePaymentMethod


class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'name', 'email', 'phone', 'country', 'is_active', 'created_on']
    list_filter = ['is_active']


class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'account_type', 'business_type', 'email', 'is_active', 'created_on']
    list_filter = ['is_active']


class StripeAcceptedCountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'country']


class StripePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'is_active', 'created_on']
    list_filter = ['is_active']


admin.site.register(StripeCustomer, StripeCustomerAdmin)
admin.site.register(StripeAccount, StripeAccountAdmin)
admin.site.register(StripeAcceptedCountry, StripeAcceptedCountryAdmin)
admin.site.register(StripePaymentMethod, StripePaymentMethodAdmin)
