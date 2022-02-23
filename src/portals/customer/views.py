from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, CreateView
from src.accounts.decorators import customer_required
from src.portals.admins.models import (
    Withdrawal, Transaction, TopUp, PaymentMethod
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
class TransactionCreateView(View):
    template_name = 'customer/transaction_create.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):

        error_message = None
        sender_wallet = request.user.get_user_wallet()
        receiver_wallet = request.POST['receiver_wallet']
        amount = request.POST['amount']
        payment_method = request.POST['payment_method']

        # CHECK0: Empty and Amount

        if receiver_wallet and amount and payment_method:
            amount = float(amount)
            if sender_wallet.amount > amount:
                # CHECK1:: receiver wallet exists
                try:

                    receiver_wallet = Wallet.objects.get(pk=receiver_wallet)
                    sender_wallet.amount -= amount
                    sender_wallet.total_transactions_amount_sent += amount
                    sender_wallet.total_transactions_sent += 1
                    sender_wallet.save()

                    receiver_wallet.amount += amount
                    receiver_wallet.total_transactions_amount_received += amount
                    receiver_wallet.total_transactions_received += 1
                    receiver_wallet.save()

                    transaction = Transaction.objects.create(
                        sender_wallet=sender_wallet, receiver_wallet=receiver_wallet, amount=amount, status='com'
                    )

                    messages.success(request, f"Amount {amount} successfully transferred to receiver {receiver_wallet.pk}")
                    return redirect("customer-portal:transaction-detail")

                except Wallet.DoesNotExist:
                    error_message = "Requested Wallet Address doesn't exists."
            else:
                error_message = "You don't have much amount to transfer"
        else:
            error_message = "Please Fill all the fields"

        messages.error(request, error_message)
        return render(request, template_name=self.template_name, context=self.context)


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

