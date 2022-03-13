import stripe

from cocognite import settings


# CREATE ACCOUNT [POST]
def stripe_connect_account_create():
    url = '/v1/accounts/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    response = stripe.Account.create(
        type="express",
        country="UK",
        email="ikram.khan0762@gmail.com",
    )
    print(response)


def stripe_account_create_link():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.AccountLink.create(
        account="acct_1032D82eZvKYlo2C",
        refresh_url="https://example.com/reauth",
        return_url="https://example.com/return",
        type="account_onboarding",
    )