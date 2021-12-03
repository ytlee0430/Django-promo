from rest_framework import serializers
from emqapi.api.models import CustomerPromoCode


class UsedCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPromoCode
        fields = ['customer_code', 'promo_code', 'transfer']


class RedeemCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPromoCode
        fields = ['customer_code', 'promo_code']
