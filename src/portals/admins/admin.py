from django.contrib import admin

from .models import (
    PaymentMethod, TopUp, Transaction, Withdrawal
)


class TopUpAdmin(admin.ModelAdmin):
    list_display = ['id', 'stripe_payment_intent', 'status', 'payment_method']


admin.site.register(PaymentMethod)
admin.site.register(TopUp, TopUpAdmin)
admin.site.register(Transaction)
admin.site.register(Withdrawal)

