
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView
from src.accounts.decorators import customer_required
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

