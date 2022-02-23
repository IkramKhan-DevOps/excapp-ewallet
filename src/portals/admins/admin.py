from django.contrib import admin

from .models import (
    PaymentMethod, TopUp, Transaction, Withdrawal
)


admin.site.register(PaymentMethod)
admin.site.register(TopUp)
admin.site.register(Transaction)
admin.site.register(Withdrawal)

