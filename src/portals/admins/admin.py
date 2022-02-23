from django.contrib import admin

from .models import (
    PaymentMethod, TopUp, Transactions, Withdrawal
)


admin.site.register(PaymentMethod)
admin.site.register(TopUp)
admin.site.register(Transactions)
admin.site.register(Withdrawal)

