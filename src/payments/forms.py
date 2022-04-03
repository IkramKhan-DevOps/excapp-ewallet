from django.forms import ModelForm
from src.payments.models import Connect, ExternalAccount


class ConnectCreateForm(ModelForm):
    class Meta:
        model = Connect
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'country', 'city', 'postal_code', 'address'
        ]


class ConnectUpdateForm(ModelForm):
    class Meta:
        model = Connect
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'city', 'postal_code', 'address'
        ]


class ExternalAccountCreateForm(ModelForm):
    class Meta:
        model = ExternalAccount
        fields = [
            'country', 'account_holder_name', 'routing_number', 'account_number'
        ]


class ExternalAccountUpdateForm(ModelForm):
    class Meta:
        model = ExternalAccount
        fields = [
            'country', 'account_holder_name', 'routing_number', 'account_number'
        ]

