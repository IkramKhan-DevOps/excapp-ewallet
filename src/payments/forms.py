from django.forms import ModelForm
from src.payments.models import Connect


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

