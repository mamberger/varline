import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Referral(User):
    phone = models.CharField(max_length=30)
    site = models.URLField()
    note = models.TextField(blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4())
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return f'{self.username} -> {self.token}'

    class Meta:
        verbose_name = 'partner'
        verbose_name_plural = 'partners'


class ReferralUser(models.Model):
    ref_token = models.UUIDField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    download = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    paid = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0))


class ModalPage(models.Model):
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=1)
    content = HTMLField()

    def __str__(self):
        return self.name
