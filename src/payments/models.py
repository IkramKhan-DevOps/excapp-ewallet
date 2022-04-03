from django.db import models
from django_resized import ResizedImageField

STRIPE_ACCOUNT_TYPE_CHOICES = (
    ('s', "Standard"),
    ('e', "Express"),
    ('c', "Custom"),
)

STRIPE_BUSINESS_TYPE_CHOICES = (
    ('i', "Individual"),
    ('c', "Company"),
    ('n', "Non-Profit"),
    ('g', "Government Entity"),
)

STRIPE_PAYMENT_TYPE_CHOICES = (
    ('w', "Wallet"),
    ('c', "Card"),
    ('b', "Bank Account"),
)


class StripeAcceptedCountry(models.Model):
    country = models.ForeignKey('admins.Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.country.name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Stripe Accepted Countries"


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('admins.Country', on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name


class Connect(models.Model):
    BUSINESS_TYPE_CHOICE = (
        ('individual', 'individual'),
    )
    connect_id = models.CharField(max_length=1000, null=True, blank=True, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=255, help_text="First Name for user")
    last_name = models.CharField(max_length=255, help_text="First Name for user")
    email = models.EmailField(help_text="Your professional email that will be linked with connect account")
    phone = models.CharField(max_length=15, help_text="Phone number that will be linked with connect account")

    country = models.ForeignKey(
        StripeAcceptedCountry, on_delete=models.SET_NULL, null=True, blank=False,
        help_text="Select the country in which you reside now, according to your according payments methods, wallets "
                  "and bank accounts will be visible"
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, help_text="Select your city", null=True, blank=True)

    postal_code = models.CharField(
        max_length=255, null=True, blank=True, help_text="Postal code according to your country and city"
    )
    address = models.TextField(null=True, blank=True, help_text="Your home or office address.")
    description = models.CharField(max_length=5000, null=True, blank=True)
    business_type = models.CharField(max_length=255, choices=BUSINESS_TYPE_CHOICE, default='individual')

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Stripe Customer'

    def __str__(self):
        return self.user.username

    def get_external_accounts(self):
        return self.externalaccount_set.all()


class ExternalAccount(models.Model):
    BUSINESS_TYPE_CHOICE = (
        ('individual', 'individual'),
    )
    ACCOUNT_TYPE_CHOICE = (
        ('card', 'Card'),
        ('bank', 'Bank'),
    )
    connect = models.ForeignKey(Connect, on_delete=models.CASCADE)
    country = models.ForeignKey(
        StripeAcceptedCountry, on_delete=models.SET_NULL, blank=False, null=True,
        help_text="Select Bank/Card Country Name"
    )
    currency = models.ForeignKey(
        Currency, blank=False, null=True, on_delete=models.SET_NULL,
        help_text="Select Currency according to your account"
    )
    account_holder_name = models.CharField(
        max_length=255, blank=False, help_text="Your full name on card or bank account"
    )
    account_holder_type = models.CharField(
        max_length=255, choices=BUSINESS_TYPE_CHOICE, default='individual',
    )
    account_type = models.CharField(
        max_length=255, choices=ACCOUNT_TYPE_CHOICE, default='bank',
    )
    routing_number = models.CharField(max_length=255, blank=False)
    account_number = models.CharField(max_length=255, blank=False)

    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'External Account'

    def __str__(self):
        return str(self.connect.connect_id)

