from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from notifications.signals import notify

from src.accounts.decorators import customer_required
from src.payments.bll import stripe_account_delete, stripe_account_create, stripe_account_get, stripe_account_update, \
    stripe_countries_list, stripe_country_get, create_customer, stripe_customer_get, stripe_customer_update, \
    stripe_customer_delete, stripe_connect_bank_accounts_list, stripe_payment_method_create, \
    stripe_payment_method_attach, stripe_setup_pay, stripe_payout_create, stripe_connect_account_create, \
    stripe_external_account_add, stripe_error_filters, stripe_payout, stripe_account_transfer, \
    stripe_get_balance
from src.payments.models import Connect
from src.portals.admins.bll import generate_qr_code, check_sanction_for_web
from src.portals.admins.models import (
    Withdrawal, Transaction, TopUp, PaymentMethod,
    Ticket, Country)
from src.accounts.models import (
    Wallet, UserSanction
)
from src.portals.customer.forms import WithdrawalForm

User = get_user_model()

customer_decorators = [login_required, customer_required]
customer_nocache_decorators = [login_required, customer_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(customer_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'customer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['wallet'] = self.request.user.get_user_wallet()
        context['transactions_list'] = Transaction.objects.filter(
            Q(sender_wallet__user=self.request.user) | Q(receiver_wallet__user=self.request.user)
        )[:10]
        context['top_up_list'] = TopUp.objects.filter(wallet__user=self.request.user)[:10]
        context['withdrawal_list'] = Withdrawal.objects.filter(wallet__user=self.request.user)[:10]

        account_id = "acct_1KjM822cdRjpWk9K"
        bank_id = "ba_1KjMAW2cdRjpWk9KRoa2WwV8"

        # stripe_get_balance()
        # stripe_connect_account_create("gbp3@uk.com", "UK", "3")
        # stripe_external_account_add(account_id)
        # stripe_account_transfer(account_id)
        # stripe_payout(account_id, bank_id)
        return context


@method_decorator(customer_nocache_decorators, name='dispatch')
class WalletGenerateQRCodeView(View):

    def get(self, request, pk):
        wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
        generate_qr_code(wallet)
        return redirect('customer-portal:wallet-detail')


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class WalletDetailView(DetailView):
    model = Wallet
    template_name = 'customer/wallet_detail.html'

    def get_object(self, queryset=None):
        return self.request.user.get_user_wallet()

    def get_context_data(self, **kwargs):
        context = super(WalletDetailView, self).get_context_data(**kwargs)
        context['sanction_form'] = self.request.user.get_user_sanctions()
        return context


@method_decorator(customer_decorators, name='dispatch')
class UserSanctionsUpdateView(View):

    def post(self, request, *args, **kwargs):
        user_sanction = UserSanction.objects.get(user=self.request.user)
        _is_app_allowed = request.POST.get('is_app_allowed')
        _is_top_up_allowed = request.POST.get('is_top_up_allowed')
        _is_transaction_allowed = request.POST.get('is_transaction_allowed')
        _is_withdrawal_allowed = request.POST.get('is_withdrawal_allowed')

        user_sanction.is_app_allowed = False
        user_sanction.is_transaction_allowed = False
        user_sanction.is_withdrawal_allowed = False
        user_sanction.is_top_up_allowed = False

        if _is_app_allowed is not None:
            user_sanction.is_app_allowed = True

        if _is_top_up_allowed is not None:
            user_sanction.is_top_up_allowed = True

        if _is_transaction_allowed is not None:
            user_sanction.is_transaction_allowed = True

        if _is_withdrawal_allowed is not None:
            user_sanction.is_withdrawal_allowed = True

        user_sanction.save()
        messages.success(request, f"{self.request.user} permissions updated successfully.")
        return redirect('customer-portal:wallet-detail')


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class TopUpListView(ListView):
    template_name = 'customer/topup_list.html'
    paginate_by = 25

    def get_queryset(self):
        return TopUp.objects.filter(wallet__user=self.request.user)


@method_decorator(customer_required, name='dispatch')
class TopUpCreateView(CreateView):
    model = TopUp
    fields = ['total']
    template_name = 'customer/topup_create.html'

    def dispatch(self, *args, **kwargs):
        if not check_sanction_for_web(self.request.user.get_user_sanctions(), 'top_up'):
            messages.error(self.request, "You don't have permission to perform any Top Up.")
            return redirect('customer-portal:topup-list')
        return super(TopUpCreateView, self).dispatch(self.request)

    def form_valid(self, form):
        form.instance.wallet = self.request.user.get_user_wallet()
        form.instance.received = 0
        form.instance.tax = 0
        return super(TopUpCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment-stripe:stripe-balance-load', args=(self.object.pk,))


@method_decorator(customer_required, name='dispatch')
class TopUpDetailView(DetailView):
    model = TopUp
    template_name = 'customer/topup_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            TopUp.objects.filter(wallet__user=self.request.user), pk=self.kwargs['pk']
        )


@method_decorator(customer_required, name='dispatch')
class TopUpInvoiceView(DetailView):
    template_name = 'customer/invoice/topup_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            TopUp.objects.filter(wallet__user=self.request.user, status='com'), pk=self.kwargs['pk']
        )


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class TransactionListView(ListView):
    template_name = 'customer/transaction_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Transaction.objects.filter(
            Q(sender_wallet__user=self.request.user) | Q(receiver_wallet__user=self.request.user)
        )


@method_decorator(customer_required, name='dispatch')
class TransactionCreateView(View):
    template_name = 'customer/transaction_create.html'
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if not check_sanction_for_web(request.user.get_user_sanctions(), 'transaction'):
            messages.error(request, "You don't have permission to perform any transaction.")
            return redirect('customer-portal:transaction-list')
        return super(TransactionCreateView, self).dispatch(request)

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
                    if sender_wallet.user != receiver_wallet.user:
                        sender_wallet.amount -= amount
                        sender_wallet.total_transactions_amount_sent += amount
                        sender_wallet.total_transactions_sent += 1
                        sender_wallet.save()

                        receiver_wallet.amount += amount
                        receiver_wallet.total_transactions_amount_received += amount
                        receiver_wallet.total_transactions_received += 1
                        receiver_wallet.save()

                        transaction = Transaction.objects.create(
                            sender_wallet=sender_wallet, receiver_wallet=receiver_wallet, total=amount,
                            status='com',
                            received=amount, tax=0
                        )

                        # TODO: notification
                        notify.send(
                            request.user,
                            recipient=sender_wallet.user,
                            verb=f'Funds Transferred',
                            level='info',
                            description=f"You have successfully transferred an amount of ${amount} to ${receiver_wallet.user.username}"
                        )
                        # ------------------
                        # TODO: notification
                        notify.send(
                            request.user,
                            recipient=receiver_wallet.user,
                            verb=f'Funds Received',
                            level='info',
                            description=f"You have received an amount of ${amount} from ${sender_wallet.user.username}"
                        )
                        # ------------------
                        # TODO: calculate_charges + bll
                        messages.success(request,
                                         f"Amount {amount} successfully transferred to receiver {receiver_wallet.pk}")
                        return redirect("customer-portal:transaction-detail", transaction.pk)

                    else:
                        error_message = "Looks like that's your wallet"
                except Wallet.DoesNotExist:
                    error_message = "Requested Wallet Address doesn't exists."
            else:
                error_message = "You don't have much amount to transfer"
        else:
            error_message = "Please Fill all the fields"

        messages.error(request, error_message)
        return render(request, template_name=self.template_name, context=self.context)


@method_decorator(customer_required, name='dispatch')
class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'customer/transaction_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.filter(
                Q(sender_wallet__user=self.request.user) | Q(receiver_wallet__user=self.request.user)
            ), pk=self.kwargs['pk']
        )


@method_decorator(customer_required, name='dispatch')
class TransactionInvoiceView(DetailView):
    template_name = 'customer/invoice/transaction_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.filter(
                Q(sender_wallet__user=self.request.user) | Q(receiver_wallet__user=self.request.user)
            ).filter(status='com'), pk=self.kwargs['pk']
        )


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class WithdrawalListView(ListView):
    template_name = 'customer/withdrawal_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Withdrawal.objects.filter(wallet__user=self.request.user)


@method_decorator(customer_required, name='dispatch')
class WithdrawalDetailView(DetailView):
    model = Withdrawal
    template_name = 'customer/withdrawal_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Withdrawal.objects.filter(wallet__user=self.request.user), pk=self.kwargs['pk'])


@method_decorator(customer_required, name='dispatch')
class WithdrawalInvoiceView(DetailView):
    model = Withdrawal
    template_name = 'customer/invoice/withdrawal_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Withdrawal.objects.filter(wallet__user=self.request.user), pk=self.kwargs['pk'])


@method_decorator(customer_required, name='dispatch')
class WithdrawalCreateView(View):
    template_name = 'customer/withdrawal_create.html'
    form_class = WithdrawalForm
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if not check_sanction_for_web(request.user.get_user_sanctions(), 'withdrawal'):
            messages.error(request, "You don't have permission to perform any withdrawal.")
            return redirect('customer-portal:withdrawal-list')
        return super(WithdrawalCreateView, self).dispatch(request)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            message_error = None
            amount = float(form.cleaned_data['total'])
            account_number = form.cleaned_data['account_number']
            wallet = self.request.user.get_user_wallet()

            # TODO: logic here
            if wallet.amount > amount:

                wallet.amount -= amount
                wallet.total_withdrawal_amount += amount
                wallet.total_withdrawal += 1
                wallet.save()

                form.instance.status = 'com'
                form.instance.wallet = wallet
                form.instance.tax = 0
                form.instance.received = amount
                withdrawal = form.save()
                messages.success(request, f"Amount {amount} successfully withdrawed to {account_number}")
                return redirect("customer-portal:withdrawal-detail", withdrawal.pk)
            else:
                message_error = "You don't have sufficient amount to withdraw"
            messages.error(request, message_error)

        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):

        self.context['form'] = self.form_class
        self.context['countries'] = Country.objects.all()
        return render(request, self.template_name, self.context)


""" ---------------------------------------------------------------------------------------------------------------- """


@method_decorator(customer_required, name='dispatch')
class TicketListView(ListView):
    template_name = 'customer/ticket_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


@method_decorator(customer_required, name='dispatch')
class TicketCreateView(CreateView):
    template_name = 'customer/ticket_create.html'
    model = Ticket
    fields = ['ticket_type', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        # TODO: notification
        notify.send(
            self.request.user,
            recipient=self.request.user,
            verb=f'Ticket Created',
            level='info',
            description=f"Your ticket has been created successfully, support team will contact you on your email."
        )
        # ------------------
        return super(TicketCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('customer-portal:ticket-list')


@method_decorator(customer_required, name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'customer/ticket_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Ticket.objects.filter(user=self.request.user), pk=self.kwargs['pk']
        )


""" -------------------------------------------------------------------------------------------------"""


# @method_decorator(customer_required, name='dispatch')
# class ConnectAccountView(DetailView):
#     model = Connect
#     template_name = 'customer/connect_account.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         stripe_customer = Connect.objects.filter(user=self.request.user)
#         if not stripe_customer:
#             messages.error(request, "Please create your connect account first")
#             return redirect("customer-portal:stripe-customer-account-create")
#         return super(ConnectAccountView, self).dispatch(request)
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Connect.objects.filter(user=self.request.user))
#
#
# @method_decorator(customer_required, name='dispatch')
# class ConnectAccountCreateView(CreateView):
#     model = Connect
#     template_name = 'customer/connect_account_create_form.html'
#     fields = ['name', 'email', 'phone', 'country']
#     success_url = reverse_lazy('customer-portal:stripe-customer-account')
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_stripe_account_exists():
#             messages.warning(request, "Connect Account is already created")
#             return redirect('customer-portal:stripe-customer-account')
#         return super(ConnectAccountCreateView, self).dispatch(request)
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(ConnectAccountCreateView, self).form_valid(form)
#
#
# @method_decorator(customer_required, name='dispatch')
# class ConnectAccountUpdateView(UpdateView):
#     model = Connect
#     template_name = 'customer/connect_account_update_form.html'
#     fields = ['name', 'email', 'phone', 'country']
#     success_url = reverse_lazy('customer-portal:stripe-customer-account')
#
#     def dispatch(self, request, *args, **kwargs):
#         stripe_customer = Connect.objects.filter(user=self.request.user)
#         if not stripe_customer:
#             messages.error(request, "Please create your connect account first")
#             return redirect("customer-portal:stripe-customer-account-create")
#         return super(ConnectAccountUpdateView, self).dispatch(request)
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Connect.objects.filter(user=self.request.user, pk=self.kwargs['pk']))
#
#
# @method_decorator(customer_required, name='dispatch')
# class ConnectAccountDeleteView(DeleteView):
#
#     template_name = 'customer/connect_account_delete.html'
#     success_url = reverse_lazy('customer-portal:stripe-customer-account')
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Connect.objects.filter(user=self.request.user, pk=self.kwargs['pk']))

""" -------------------------------------------------------------------------------------------------"""
