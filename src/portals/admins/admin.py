from django.contrib import admin

from .models import (
    PaymentMethod, TopUp, Transaction, Withdrawal, Country
)


class TopUpAdmin(admin.ModelAdmin):
    list_display = ['id', 'total', 'tax', 'received', 'wallet', 'payment_method', 'is_active', 'created_on']
    search_fields = ['id', 'wallet']
    list_filter = ['payment_method', 'is_active']


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'total', 'tax', 'received', 'sender_wallet',
        'receiver_wallet', 'type', 'status', 'is_active',
        'created_on'
    ]
    search_fields = ['id']
    list_filter = ['status', 'is_active']


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'total', 'tax', 'received', 'wallet',
        'account_number', 'bank_name', 'status', 'is_active',
        'created_on'
    ]
    search_fields = ['id']
    list_filter = ['status', 'is_active']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    search_fields = ['id', 'name']
    list_filter = ['is_active']


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon', 'country', 'is_active']
    search_fields = ['id', 'name', 'country']
    list_filter = ['is_active', 'country']


admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(TopUp, TopUpAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)

