import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField


class User(AbstractUser):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )

    is_customer = models.BooleanField(default=True, help_text="This account belongs to customer")

    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[200, 200], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE)
    about = models.TextField(null=True, blank=True, help_text="Tell us something interesting about yourself")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)

    def get_user_wallet(self):
        return Wallet.objects.get(user=self)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    code = models.UUIDField(max_length=1000, default=uuid.uuid4, unique=True, editable=False)

    total_top_up_amount = models.FloatField(default=0)
    total_transactions_amount = models.FloatField(default=0)
    total_withdrawal_amount = models.FloatField(default=0)

    total_top_up = models.PositiveIntegerField(default=0)
    total_transactions = models.PositiveIntegerField(default=0)
    total_withdrawal = models.PositiveIntegerField(default=0)

    top_up_limit = models.IntegerField(default=0)
    transaction_limit = models.IntegerField(default=10000)
    withdrawal_limit = models.IntegerField(default=10000)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User, dispatch_uid="user_wallet_add")
def create_wallet_for_user(sender, instance, **kwargs):
    Wallet.objects.create(user=instance)
