import json

import stripe
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from notifications.signals import notify

from cocognite import settings
from src.accounts.models import Wallet
from src.portals.admins.models import TopUp

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
def create_checkout_session2(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

            # If we want to identify the user when using webhooks we can pass client_reference_id  to checkout
            # session constructor. We will then be able to fetch it and make changes to our Django models.
            #
            # If we offer a SaaS service it would also be good to allow only authenticated users to purchase
            # anything on our site.

            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Vat - 176+',
                        'quantity': 1,
                        'currency': 'eur',
                        'amount': 17600,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


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
