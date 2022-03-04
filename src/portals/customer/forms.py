from django.forms import ModelForm

from src.accounts.models import UserSanction
from src.portals.admins.models import Withdrawal


class WithdrawalForm(ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['total', 'bank_name', 'account_number', 'account_holder_name']


class UserSanctionForm(ModelForm):
    class Meta:
        model = UserSanction
        fields = ['is_app_allowed', 'is_top_up_allowed', 'is_transaction_allowed', 'is_withdrawal_allowed']

