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


class StripePaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    image = ResizedImageField(
        upload_to='portals/accounts/payment_methods/', height_field=100, width_field=200, quality=75,
        null=True, blank=True
    )

    # stripe_payment_methods_id = models.CharField(max_length=1000, unique=True, null=False, blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StripeAcceptedCountry(models.Model):
    country = models.ForeignKey('admins.Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.country.name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Stripe Accepted Countries"


class StripeCustomer(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True)
    name = models.CharField(
        max_length=255,
        help_text="Kindly! use your full correct name that must be same to your National ID, Passport or Bank Acounts"
    )
    email = models.EmailField(help_text="")
    phone = models.CharField(max_length=15, help_text="Phone number without country code")
    country = models.ForeignKey(
        StripeAcceptedCountry, on_delete=models.SET_NULL, null=True, blank=False,
        help_text="Select the country in which you reside now, according to your according payments methods, wallets "
                  "and bank accounts will be visible"
    )
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.TextField(null=True, blank=True, help_text="Postal code according to your country")
    address = models.TextField(null=True, blank=True, help_text="Your home or office address.")
    description = models.CharField(max_length=5000, null=True, blank=True)

    # customer_account_id = models.CharField(max_length=255, unique=True, null=False, blank=True)

    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Stripe Customer'

    def __str__(self):
        return self.user.username


class StripeAccount(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, blank=True)
    account_type = models.CharField(max_length=1, choices=STRIPE_ACCOUNT_TYPE_CHOICES, default='e')
    business_type = models.CharField(max_length=1, choices=STRIPE_BUSINESS_TYPE_CHOICES, default='i')
    email = models.EmailField()

    # connect_account_id = models.CharField(max_length=255, unique=True, null=False, blank=True)

    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Stripe Account'

    def __str__(self):
        return self.user.username
