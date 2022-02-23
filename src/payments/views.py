import stripe
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from cocognite import settings

""" STRIPE REQUESTS"""


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Sole Traders',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 9000,
        }],
        mode='payment',
        success_url=domain_url + 'success/',
        cancel_url=domain_url + 'cancelled/',
    )

    return redirect(session.url, code=303)


@csrf_exempt
def create_checkout_session_280(request):
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Limited Companies',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 28000,
        }],
        mode='payment',
        success_url=domain_url + 'success/',
        cancel_url=domain_url + 'cancelled/',
    )

    return redirect(session.url, code=303)


@csrf_exempt
def create_checkout_session_40(request):
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Dormant Accounts',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 3500,
        }],
        mode='payment',
        success_url=domain_url + 'success/',
        cancel_url=domain_url + 'cancelled/',
    )

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


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'
