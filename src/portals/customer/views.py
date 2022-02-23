from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, CreateView
from src.accounts.decorators import customer_required
from src.portals.admins.models import (
    Withdrawal, Transactions, TopUp, PaymentMethod
)
from src.accounts.models import (
    Wallet
)

User = get_user_model()

customer_decorators = [login_required, customer_required]
customer_nocache_decorators = [login_required, customer_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(customer_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'customer/dashboard.html'


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class WalletDetailView(TemplateView):
    template_name = 'customer/wallet_detail.html'


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class TopUpListView(TemplateView):
    template_name = 'customer/topup_list.html'


@method_decorator(customer_required, name='dispatch')
class TopUpCreateView(CreateView):
    model = TopUp
    fields = ['amount']
    template_name = 'customer/topup_create.html'

    def form_valid(self, form):
        form.instance.wallet = self.request.user.get_user_wallet()
        return super(TopUpCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment-stripe:stripe-balance-load', args=(self.object.pk, ))


@method_decorator(customer_required, name='dispatch')
class TopUpDetailView(TemplateView):
    template_name = 'customer/topup_detail.html'


@method_decorator(customer_required, name='dispatch')
class TopUpInvoiceView(TemplateView):
    template_name = 'customer/invoice/topup_invoice.html'


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class TransactionListView(TemplateView):
    template_name = 'customer/transaction_list.html'


@method_decorator(customer_required, name='dispatch')
class TransactionDetailView(TemplateView):
    template_name = 'customer/transaction_detail.html'


@method_decorator(customer_required, name='dispatch')
class TransactionInvoiceView(TemplateView):
    template_name = 'customer/invoice/transaction_invoice.html'


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class WithdrawalListView(TemplateView):
    template_name = 'customer/withdrawal_list.html'


@method_decorator(customer_required, name='dispatch')
class WithdrawalDetailView(TemplateView):
    template_name = 'customer/withdrawal_detail.html'


@method_decorator(customer_required, name='dispatch')
class WithdrawalInvoiceView(TemplateView):
    template_name = 'customer/invoice/withdrawal_invoice.html'

