from datetime import datetime

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from emqapi.api.models import PromoCode, CustomerPromoCode


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'


class CustomerPromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPromoCode
        fields = '__all__'


class CustomerPromoCodeListSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField('is_expire')
    enabled = serializers.SerializerMethodField('is_enable')
    expired_time = serializers.SerializerMethodField('get_promo_code_expired_time')
    promo_code_meta_data = serializers.SerializerMethodField('get_promo_code_meta_data')

    def is_expire(self, customer_promo_code):
        promo_code = customer_promo_code.promo_code
        return promo_code.valid_end_date is not None \
               and promo_code.valid_end_date.replace(tzinfo=None) < datetime.utcnow()

    def is_enable(self, customer_promo_code):
        promo_code = customer_promo_code.promo_code
        if promo_code.valid_start_date is not None \
               and promo_code.valid_start_date.replace(tzinfo=None) > datetime.utcnow():
            return False
        if not promo_code.enabled:
            return False

    def get_promo_code_meta_data(self, customer_promo_code):
        promo_code = customer_promo_code.promo_code
        return promo_code.meta_data

    def get_promo_code_expired_time(self, customer_promo_code):
        return customer_promo_code.promo_code.valid_end_date

    class Meta:
        model = CustomerPromoCode
        fields = ['customer_code', 'promo_code', 'redeem_time',
                  'used', 'expired', 'enabled', 'promo_code_meta_data', 'expired_time']
