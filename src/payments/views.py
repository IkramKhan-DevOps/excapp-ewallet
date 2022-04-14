import json

import requests
import stripe
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, DeleteView, ListView
from notifications.signals import notify

from cocognite import settings
from src.accounts.models import Wallet
from src.payments.bll import stripe_external_bank_account_add, stripe_external_account_delete, \
    stripe_account_create_custom
from src.payments.forms import ConnectCreateForm, ConnectUpdateForm, ExternalAccountCreateForm, \
    ExternalAccountUpdateForm
from src.payments.models import Connect, ExternalAccount, StripeAcceptedCountry, City, Currency
from src.portals.admins.models import TopUp
import urllib

""" STRIPE REQUESTS"""


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    top_up = get_object_or_404(TopUp.objects.filter(wallet__user=request.user, status='pen'), pk=pk)
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Balance Top Up',
            'quantity': 1,
            'currency': 'usd',
            'amount': int(str(top_up.total) + "00"),
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment-stripe:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment-stripe:cancel')),
    )
    top_up.stripe_payment_intent = session.id
    top_up.save()

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        # product = Product.objects.get(id=product_id)

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        top_up = get_object_or_404(TopUp, stripe_payment_intent=session_id)
        top_up.status = 'com'
        top_up.received = top_up.total - top_up.tax
        top_up.save()

        wallet = Wallet.objects.get(pk=top_up.wallet.pk)
        wallet.amount += top_up.total
        wallet.total_top_up += 1
        wallet.total_top_up_amount += top_up.total
        wallet.save()

        # TODO: notification
        notify.send(
            request.user,
            recipient=wallet.user,
            verb=f'Balance Load',
            level='info',
            description=f"You have successfully deposited an amount of ${top_up.total} to your wallet."
        )
        # ------------------

        return render(request, self.template_name)


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


class ConnectAccount(DetailView):
    model = Connect


""" CONNECT ACCOUNT """
""" ---------------------------------------------------------------------------------------------------------------- """


class ConnectCreateView(View):
    template_name = 'payments/connect_form.html'
    context = {}
    form_class = ConnectCreateForm

    def get(self, request):
        self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request):

        form = ConnectCreateForm(data=request.POST)

        # 1: forms validation
        if form.is_valid():

            # from user model
            _email = request.user.email
            _last_name = request.user.last_name
            _first_name = request.user.first_name

            # from form
            _phone = form.data['phone']
            _address = form.data['address']
            _postal_code = form.data['postal_code']
            _city = get_object_or_404(City, pk=form.data['city'])
            _country = get_object_or_404(StripeAcceptedCountry, pk=form.data['country'])

            # missing handling
            if form.data['first_name'] == '':
                _first_name = request.user.first_name
            if form.data['last_name'] == '':
                _last_name = request.user.last_name

            # filling form
            form.instance.user = request.user
            form.instance.first_name = _first_name
            form.instance.last_name = _last_name
            form.instance.email = _email
            # form.save()

            # -------------------------------- API CALL TO HANDLE
            is_error, response = stripe_account_create_custom(
                email=_email, first_name=_first_name, last_name=_last_name, phone=_phone, gender='male', day=30,
                month=12,
                year=2001, country=_country.country.short_code, city=_city.name, state=_city.name,
                address_line_1=_address, postal_code=_postal_code
            )
            # ---------------------------------------------------
            if not is_error:
                form.instance.connect_id = response['id']
                form.instance.is_verified = True
                form.save()

                messages.success(request, "Connect account added successfully")
                return redirect('payment-stripe:connect')
            else:
                messages.error(request, response)

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ConnectUpdateView(View):
    template_name = 'payments/connect_form.html'
    context = {}
    form_class = ConnectUpdateForm

    def get(self, request):
        self.context['form'] = ConnectUpdateForm(instance=Connect.objects.get(user=request.user))
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ConnectUpdateForm(instance=Connect.objects.get(user=request.user), data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Connect account updated successfully")
            return redirect('payment-stripe:connect')
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ConnectDetailView(DetailView):
    template_name = 'payments/connect_detail.html'
    model = Connect

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ConnectDetailView, self).dispatch(request)

    def get_object(self, queryset=None):
        return get_object_or_404(Connect.objects.filter(), user=self.request.user)


class ConnectDeleteView(View):
    template_name = 'payments/connect_delete_confirm.html'
    model = Connect

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "You don't have any account yet.")
            return redirect('payment-stripe:connect-create')
        return super(ConnectDeleteView, self).dispatch(request)

    def get(self, request):
        context = {
            'object': request.user.get_stripe_account()
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):

        # 1: ACCOUNTS EXISTENCE
        c_account = request.user.get_stripe_account()

        # 2: IN STRIPE
        if c_account.is_verified:
            response = stripe.Account.delete(c_account.connect_id)
            print(response)

            # 3: DELETED SUCCESSFULLY
            if response['deleted']:
                c_account.delete()
                messages.success(request, "Connect account deleted successfully")
                return redirect('payment-stripe:connect')

            messages.error(request, "Failed to delete connect - api")

        else:
            c_account.delete()
            messages.success(request, "Linked external account deleted successfully")
            return redirect('payment-stripe:connect-create')

        return redirect('payment-stripe:connect')


""" EXTERNAL ACCOUNTS """


class ExternalAccountListView(ListView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ExternalAccountListView, self).dispatch(request)

    def get_queryset(self):
        return ExternalAccount.objects.filter(connect__user=self.request.user)


class ExternalAccountCreateView(View):
    template_name = 'payments/externalaccount_form.html'
    context = {}
    form_class = ExternalAccountCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ExternalAccountCreateView, self).dispatch(request)

    def get(self, request):
        self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ExternalAccountCreateForm(data=request.POST)
        _error_message = None

        # 0:: OVERALL VALIDATIONS
        if form.is_valid():
            connect_account = request.user.get_stripe_account()
            form.instance.connect = connect_account

            country = get_object_or_404(StripeAcceptedCountry, pk=request.POST['country'])
            currency = get_object_or_404(Currency, pk=request.POST['currency'])
            country_short = country.country.short_code
            currency_short = currency.short_code
            account_number = request.POST['account_number']
            routing_number = request.POST['routing_number']
            account_holder_name = request.POST['account_holder_name']

            # -------------------------------------------------
            error, response = stripe_external_bank_account_add(
                account_id=connect_account.connect_id, country=country_short, currency=currency_short,
                name=account_holder_name, routing_number=routing_number, account_number=account_number
            )
            if not error:
                form.instance.external_account_id = response['id']
                form.instance.is_verified = True
                _account = form.save()
                messages.success(request, "External account added successfully")
                return redirect('payment-stripe:connect')
            else:
                messages.error(request, response)
            # ------------------------------------------------

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ExternalAccountUpdateView(View):
    template_name = 'payments/externalaccount_form.html'
    context = {}
    form_class = ExternalAccountUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ExternalAccountUpdateView, self).dispatch(request)

    def get(self, request, *args, **kwargs):
        e_account = get_object_or_404(ExternalAccount.objects.filter(connect__user=self.request.user),
                                      pk=self.kwargs['pk'])
        self.context['form'] = ExternalAccountUpdateForm(instance=e_account)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        e_account = get_object_or_404(ExternalAccount.objects.filter(connect__user=self.request.user),
                                      pk=self.kwargs['pk'])
        form = ExternalAccountUpdateForm(instance=e_account, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "External Account updated successfully")
            return redirect('payment-stripe:connect')
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ExternalAccountDeleteView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_stripe_account_exists():
            messages.error(request, "Please create connect account first")
            return redirect('payment-stripe:connect-create')
        return super(ExternalAccountDeleteView, self).dispatch(request)

    def get(self, request):
        context = {
            'object': request.user.get_stripe_account()
        }
        return render(request, template_name='payments/externalaccount_confirm_delete.html', context=context)

    def post(self, request):

        # 1: ACCOUNTS EXISTENCE
        b_account = get_object_or_404(ExternalAccount.objects.all(), pk=self.kwargs['pk'])
        c_account = b_account.connect
        print(b_account.external_account_id)

        # 2: IN STRIPE
        if b_account.is_verified:

            # response = stripe_external_account_delete(c_account.connect_id, b_account.external_account_id)

            # 3: DELETED SUCCESSFULLY
            # if response['deleted']:
            #     b_account.delete()
            #     messages.success(request, "External account deleted successfully")
            messages.error(request, "Not allowed to delete external account")

        else:
            b_account.delete()
            messages.success(request, "Linked external account deleted successfully")

        return redirect('payment-stripe:connect')
