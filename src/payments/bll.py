from cocognite import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

""" START --------------------------------------------------------------------------------------------------------- """


def stripe_error_filters():
    pass


""" ---------------------------------------------------------------------------------------------------------------- """


def stripe_connected_account(stripe_user_id):
    return stripe.Account.retrieve(stripe_user_id)


def stripe_countries_list(limit=None):
    if limit:
        countries = stripe.CountrySpec.list(limit=limit)
    else:
        countries = stripe.CountrySpec.list()
    return countries


def stripe_country_get(name="US"):
    account = stripe.CountrySpec.retrieve(name)


""" ACCOUNTS ------------------------------------------------------------------------------------------------------- """


def stripe_account_create():
    account = stripe.Account.create(
        type="custom",
        country="US",
        email="email@email.com",
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
    )


""" PAYOUTS -------------------------------------------------------------------------------------------------------- """


def stripe_payout_create(amount, bank_account, currency="usd"):
    response = stripe.Payout.create(amount=amount, currency=currency, destination=bank_account)
    print(response)


def stripe_payout_retrieve(payout_id):
    response = stripe.Payout.retrieve(payout_id)
    print(response)


def stripe_payout_get(payout_id):
    response = stripe.Payout.retrieve(payout_id)
    print(response)


def stripe_payout_cancel(payout_id):
    response = stripe.Payout.cancel(payout_id)
    print(response)


""" BANK ACCOUNTS CONNECTED ---------------------------------------------------------------------------------------- """


def stripe_connect_bank_accounts_list(customer):
    response = stripe.Customer.list_payment_methods(customer, type="card")
    print(response)


def stripe_payment_method_create(customer):
    response = stripe.Customer.list_sources(
        customer,
        object="bank_account",
        limit=10,
    )
    print(response)


def stripe_payment_method_update(customer, bank_account):
    response = stripe.Customer.modify_source(
        customer,
        bank_account,
        metadata={"order_id": "6735"},
    )
    print(response)


def stripe_payment_method_delete(customer, bank_account):
    response = stripe.Customer.delete_source(
        "cus_LMSQcY9swpIK0E",
        "ba_1KfjVGGWh1G1v77h0iQu37nM",
    )
    print(response)


""" ---------------------------------------------------------------------------------------------------------------- """
