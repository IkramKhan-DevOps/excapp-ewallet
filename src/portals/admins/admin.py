from django.contrib import admin

from src.accounts.models import UserSanction
from .models import (
    PaymentMethod, TopUp, Transaction, Withdrawal, Country,
    TicketType, Ticket)


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


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'priority']
    search_fields = ['id', 'name']
    list_filter = ['priority']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_completed', 'is_active', 'created_on']
    search_fields = ['id', 'user']
    list_filter = ['is_active', 'is_completed', 'ticket_type']


admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(TopUp, TopUpAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
admin.site.register(UserSanction)
admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)

