from cocognite import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

""" START --------------------------------------------------------------------------------------------------------- """


def stripe_error_filters():
    try:
        response = stripe.Account.create(
            type="express",
            country="US",
            email="ikram.khan07622@gmail.com",
            business_type="individual",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
            individual={
                "email": "ikram.khan07622@gmail.com",
                "first_name": "Ikram",
                "gender": "male",
                "last_name": "Khans",
            }
        )
        print(response)

    except stripe.error.CardError as e:
        print('Status is: %s' % e.http_status)
        print('Code is: %s' % e.code)
        print('Param is: %s' % e.param)
        print('Message is: %s' % e.user_message)
    except stripe.error.RateLimitError as e:
        print(e)
    except stripe.error.InvalidRequestError as e:
        print(e)
    except stripe.error.AuthenticationError as e:
        print(e)
    except stripe.error.APIConnectionError as e:
        print(e)
    except stripe.error.StripeError as e:
        print(e)
    except Exception as e:
        print(e)


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
    response = stripe.Payout.create(
        amount=amount,
        currency=currency,
        destination=bank_account
    )
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


# FINE
def stripe_setup_pay():
    response = stripe.SetupIntent.create(
        payment_method_types=["card"],
    )
    print(response)


""" =================================================================================================== """


def stripe_connect_account_create():
    response = stripe.Account.create(
        type="express",
        country="US",
        email="ikram.khan07622@gmail.com",
        business_type="individual",
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
        individual={
            "address": "fake address",
            "email": "ikram.khan07622@gmail.com",
            "first_name": "Ikram",
            "gender": "male",
            "last_name": "Khans",
        }
    )
    print(response)


def stripe_external_account_add(account_id="acct_1Khrk12eTaL0y3sK"):
    response = stripe.Account.create_external_account(
        account_id,
        external_account={
            "object": "bank_account",
            "country": "US",
            "currency": "usd",
            "account_holder_name": "Ikram Khan",
            "account_holder_type": "individual",
            "routing_number": "110000000",
            "account_number": "000123456789",
        }
    )
    print(response)


def stripe_to_stripe(account_id="acct_1Khrk12eTaL0y3sK"):
    response = stripe.Transfer.create(
        amount=100,
        currency="usd",
        destination=account_id,
        transfer_group="ORDER_95",
    )
    print(response)


def stripe_payout(account_id="acct_1Khrk12eTaL0y3sK"):
    response = stripe.Payout.create(amount=1100, currency="usd", destination="ba_1Khrpr2eTaL0y3sKkeC5wT6o")
    print(response)

# v = {
#     "business_profile": {
#         "mcc": null,
#         "name": null,
#         "product_description": null,
#         "support_address": null,
#         "support_email": null,
#         "support_phone": null,
#         "support_url": null,
#         "url": null
#     },
#     "business_type": "individual",
#     "capabilities": {
#         "card_payments": "inactive",
#         "transfers": "inactive"
#     },
#     "charges_enabled": false,
#     "company": {
#         "address": {
#             "city": null,
#             "country": "US",
#             "line1": null,
#             "line2": null,
#             "postal_code": null,
#             "state": null
#         },
#         "directors_provided": true,
#         "executives_provided": true,
#         "name": null,
#         "owners_provided": true,
#         "tax_id_provided": false,
#         "verification": {
#             "document": {
#                 "back": null,
#                 "details": null,
#                 "details_code": null,
#                 "front": null
#             }
#         }
#     },
#     "country": "US",
#     "created": 1648367737,
#     "default_currency": "usd",
#     "details_submitted": false,
#     "email": "ikram.khan0762@gmail.com",
#     "external_accounts": {
#         "data": [],
#         "has_more": false,
#         "object": "list",
#         "total_count": 0,
#         "url": "/v1/accounts/acct_1KhqwnGhJD0zkSfg/external_accounts"
#     },
#     "future_requirements": {
#         "alternatives": [],
#         "current_deadline": null,
#         "currently_due": [],
#         "disabled_reason": null,
#         "errors": [],
#         "eventually_due": [],
#         "past_due": [],
#         "pending_verification": []
#     },
#     "id": "acct_1KhqwnGhJD0zkSfg",
#     "login_links": {
#         "data": [],
#         "has_more": false,
#         "object": "list",
#         "total_count": 0,
#         "url": "/v1/accounts/acct_1KhqwnGhJD0zkSfg/login_links"
#     },
#     "metadata": {},
#     "object": "account",
#     "payouts_enabled": false,
#     "requirements": {
#         "alternatives": [],
#         "current_deadline": null,
#         "currently_due": [
#             "business_profile.mcc",
#             "business_profile.url",
#             "external_account",
#             "individual.address.city",
#             "individual.address.line1",
#             "individual.address.postal_code",
#             "individual.address.state",
#             "individual.dob.day",
#             "individual.dob.month",
#             "individual.dob.year",
#             "individual.email",
#             "individual.first_name",
#             "individual.id_number",
#             "individual.last_name",
#             "individual.phone",
#             "tos_acceptance.date",
#             "tos_acceptance.ip"
#         ],
#         "disabled_reason": "requirements.past_due",
#         "errors": [],
#         "eventually_due": [
#             "business_profile.mcc",
#             "business_profile.url",
#             "external_account",
#             "individual.address.city",
#             "individual.address.line1",
#             "individual.address.postal_code",
#             "individual.address.state",
#             "individual.dob.day",
#             "individual.dob.month",
#             "individual.dob.year",
#             "individual.email",
#             "individual.first_name",
#             "individual.id_number",
#             "individual.last_name",
#             "individual.phone",
#             "tos_acceptance.date",
#             "tos_acceptance.ip"
#         ],
#         "past_due": [
#             "business_profile.mcc",
#             "business_profile.url",
#             "external_account",
#             "individual.address.city",
#             "individual.address.line1",
#             "individual.address.postal_code",
#             "individual.address.state",
#             "individual.dob.day",
#             "individual.dob.month",
#             "individual.dob.year",
#             "individual.email",
#             "individual.first_name",
#             "individual.id_number",
#             "individual.last_name",
#             "individual.phone",
#             "tos_acceptance.date",
#             "tos_acceptance.ip"
#         ],
#         "pending_verification": []
#     },
#     "settings": {
#         "bacs_debit_payments": {},
#         "branding": {
#             "icon": null,
#             "logo": null,
#             "primary_color": null,
#             "secondary_color": null
#         },
#         "card_issuing": {
#             "tos_acceptance": {
#                 "date": null,
#                 "ip": null
#             }
#         },
#         "card_payments": {
#             "decline_on": {
#                 "avs_failure": false,
#                 "cvc_failure": false
#             },
#             "statement_descriptor_prefix": null
#         },
#         "dashboard": {
#             "display_name": null,
#             "timezone": "Etc/UTC"
#         },
#         "payments": {
#             "statement_descriptor": null,
#             "statement_descriptor_kana": null,
#             "statement_descriptor_kanji": null
#         },
#         "payouts": {
#             "debit_negative_balances": true,
#             "schedule": {
#                 "delay_days": 2,
#                 "interval": "daily"
#             },
#             "statement_descriptor": null
#         },
#         "sepa_debit_payments": {}
#     },
#     "tos_acceptance": {
#         "date": null,
#         "ip": null,
#         "user_agent": null
#     },
#     "type": "express"
# }
