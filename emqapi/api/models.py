import uuid
from emqapi.constants import Constants

from django.db import models


class PromoCode(models.Model):
    code = models.CharField(max_length=32, primary_key=True)
    valid_start_date = models.DateTimeField(help_text='license start date', null=True)
    valid_end_date = models.DateTimeField(help_text='license end date', null=True)
    stock = models.IntegerField(null=True)
    campaign = models.CharField(max_length=32)
    enable = models.BooleanField()
    meta_data = models.JSONField(default=dict)


class CustomerPromoCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_code = models.CharField(max_length=16)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.DO_NOTHING)
    redeem_time = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)
    transfer = models.UUIDField(default=Constants.Empty_UUID)

    class Meta:
        unique_together = ('customer_code', 'promo_code', 'transfer',)


