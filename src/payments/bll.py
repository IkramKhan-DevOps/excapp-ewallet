from cocognite import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

""" START --------------------------------------------------------------------------------------------------------- """


def stripe_error_filters():
    pass


""" ---------------------------------------------------------------------------------------------------------------- """


# WORKING FINE >>
def stripe_connected_account(stripe_user_id):
    return stripe.Account.retrieve(stripe_user_id)


# WORKING FINE >>
def stripe_countries_list(limit=None):
    if limit:
        countries = stripe.CountrySpec.list(limit=limit)
    else:
        countries = stripe.CountrySpec.list()
    return countries


# WORKING FINE >>
def stripe_country_get(name="US"):
    country = stripe.CountrySpec.retrieve(name)
    return country


""" ACCOUNTS ------------------------------------------------------------------------------------------------------- """


# WORKING FINE >>
def stripe_account_create():
    response = stripe.Account.create(
        type="custom",
        country="US",
        email="email@email.com",
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
    )
    print(response)


# WORKING FINE >>
def stripe_account_update(account_id):
    response = stripe.Account.modify(
        id=account_id,
        metadata={
            'type': "express",
            'country': "US",
            'email': "email@email.com",
            'capabilities': {
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
            'individual': {
                "first_name": "Ikram",
                "last_name": "Khan",
                "gender": "male",
                "id_number": "1350387834811",
                "phone": "04000000000",
            },
        }
    )
    print(response)


# WORKING FINE >>
def stripe_account_get(account_id):
    response = stripe.Account.retrieve(account_id)
    print(response)


# WORKING FINE >>
def stripe_account_delete(account_id):
    response = stripe.Account.delete(account_id)
    print(response['deleted'])


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


# DONE
def stripe_connect_bank_accounts_list(customer):
    response = stripe.Customer.list_payment_methods(customer, type="card")
    print(response)


# DONE >> first create then attach
def stripe_payment_method_create(customer):
    response = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 3,
            "exp_year": 2023,
            "cvc": "314",
        },
    )
    print(response)


def stripe_payment_method_attach(customer, payment_method):
    response = stripe.PaymentMethod.attach(
        payment_method,
        customer=customer,
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


def stripe_bank_account_verify(customer, bank_account):
    bank_account = stripe.Customer.retrieve_source(
        customer, bank_account
    )
    response = bank_account.verify(amounts=[32, 45])
    print(response)


""" CUSTOMER ------------------------------------------------------------------------------------------------------- """


# FINE
def create_customer():
    response = stripe.Customer.create(
        description="My First Test Customer (created for API docs)",
        email="ikram.khan079962@gmail.com",
        name="Ikram Khan",
        phone="+923005849613"
    )
    print(response)


# FINE
def stripe_customer_get(customer_id):
    response = stripe.Customer.retrieve(customer_id)
    print(response)


# FINE
def stripe_customer_update(customer_id):
    response = stripe.Customer.modify(
        customer_id,
        description="This has been updated"
    )
    print(response)


# FINE
def stripe_customer_delete(customer_id):
    response = stripe.Customer.delete(
        customer_id
    )
    print(response)

