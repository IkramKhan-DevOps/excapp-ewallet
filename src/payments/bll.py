from cocognite import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_error_filters():
    pass


# ACCOUNT INFO >>
def get_connected_account(stripe_user_id):
    return stripe.Account.retrieve(stripe_user_id)


def payout_create():
    stripe.Payout.create(amount=1100, currency="usd")
