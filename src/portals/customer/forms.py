from django.forms import ModelForm

from src.portals.admins.models import Withdrawal


class WithdrawalForm(ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['total', 'bank_name', 'account_number', 'account_holder_name']
