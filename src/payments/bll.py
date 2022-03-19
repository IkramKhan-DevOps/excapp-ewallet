from cocognite import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


""" START --------------------------------------------------------------------------------------------------------- """


def stripe_error_filters():
    pass


""" ---------------------------------------------------------------------------------------------------------------- """


def get_connected_account(stripe_user_id):
    return stripe.Account.retrieve(stripe_user_id)


def stripe_account_create():
    pass


""" ---------------------------------------------------------------------------------------------------------------- """


def stripe_payout_create(amount, currency="usd"):
    stripe.Payout.create(amount=amount, currency=currency)


def stripe_payout_get(payout_id):
    stripe.Payout.retrieve(payout_id)


def stripe_payout_cancel(payout_id):
    stripe.Payout.cancel(payout_id)


""" ---------------------------------------------------------------------------------------------------------------- """


def stripe_payment_method_list(customer_id):
    stripe.Customer.list_payment_methods(customer_id, type="card")


def stripe_payment_method_create():
    stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 3,
            "exp_year": 2023,
            "cvc": "314",
        },
    )


def stripe_payment_method_update(payment_method_id):
    stripe.PaymentMethod.modify(
        payment_method_id,
        metadata={"order_id": "6735"},
    )


""" ---------------------------------------------------------------------------------------------------------------- """
