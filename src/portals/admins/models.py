from django.db import models

from src.accounts.models import User, Wallet


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, default="bx bx-transfer")

    class Meta:
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name


class TopUp(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )

    amount = models.PositiveIntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=3)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Top Ups"

    def __str__(self):
        return str(self.pk)


class Withdrawal(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )

    amount = models.PositiveIntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True)
    bank_name = models.CharField(max_length=1000)
    bank_branch = models.CharField(max_length=1000)
    bank_account_number = models.CharField(max_length=1000)
    status = models.CharField(choices=STATUS_CHOICE, max_length=3)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Withdrawals"

    def __str__(self):
        return str(self.pk)


class Transactions(models.Model):
    STATUS_CHOICE = (
        ('com', 'Completed'),
        ('pen', 'Pending'),
        ('can', 'Cancelled'),
    )
    TYPE_CHOICE = (
        ('p2p', 'Peer To Peer'),
    )

    amount = models.PositiveIntegerField()
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, related_name='sender+')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, related_name='receiver+')
    type = models.CharField(choices=TYPE_CHOICE, max_length=3)
    status = models.CharField(choices=STATUS_CHOICE, max_length=3)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.pk)

