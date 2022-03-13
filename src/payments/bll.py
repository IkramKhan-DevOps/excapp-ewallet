import stripe

from cocognite import settings


def stripe_account_create():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Account.create(
        country="US",
        type="custom",
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
    )
