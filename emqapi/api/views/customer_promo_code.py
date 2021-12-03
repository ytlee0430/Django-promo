from datetime import datetime

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from emqapi.api.serializers import CustomerPromoCodeSerializer, CustomerPromoCodeListSerializer
from emqapi.api.models import CustomerPromoCode, PromoCode
from emqapi.constants import Constants
from emqapi.api.request_validator.used_code_validator \
    import UsedCodeSerializer, RedeemCodeSerializer


class CustomerPromoCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CustomerPromoCode.objects.all()
    serializer_class = CustomerPromoCodeSerializer
    permission_classes = [permissions.BasePermission]

    @action(detail=False, methods=['post'], permission_classes=[permissions.BasePermission])
    def redeem_code(self, request):
        data = request.data
        validatorSerializer = RedeemCodeSerializer(data=data)
        validatorSerializer.is_valid(raise_exception=True)

        promo_code = PromoCode.objects.get(code=data['promo_code'])
        if CustomerPromoCode.objects.filter(customer_code=data['customer_code'],
                                            promo_code__campaign=promo_code.campaign).exists():
            return Response(data='campaign duplicate', status=status.HTTP_400_BAD_REQUEST)
        if not promo_code.enable:
            return Response(data='promo code disabled', status=status.HTTP_400_BAD_REQUEST)
        if promo_code.valid_end_date is not None \
                and promo_code.valid_end_date.replace(tzinfo=None) < datetime.utcnow():
            return Response(data='expired', status=status.HTTP_400_BAD_REQUEST)
        if promo_code.stock is not None:
            if promo_code.stock < 1:
                return Response(data='promo code ran out', status=status.HTTP_400_BAD_REQUEST)
            promo_code.stock -= 1
            promo_code.save()

        validatorSerializer.save()
        return Response(data=validatorSerializer.data)

    @action(detail=False, methods=['put'], permission_classes=[permissions.BasePermission])
    def use_code(self, request):
        data = request.data
        validatorSerializer = UsedCodeSerializer(data=data)
        validatorSerializer.is_valid(raise_exception=True)
        try:
            customer_promo_code = CustomerPromoCode.objects.get(customer_code=data['customer_code'],
                                                                promo_code=data['promo_code'],
                                                                transfer=Constants.Empty_UUID)
        except:
            return Response(data='customer promo code not found', status=status.HTTP_404_NOT_FOUND)

        promo_code = customer_promo_code.promo_code
        if promo_code.valid_start_date is not None \
                and promo_code.valid_start_date.replace(tzinfo=None) > datetime.utcnow():
            return Response(data='not in valid time yet', status=status.HTTP_400_BAD_REQUEST)
        if promo_code.valid_end_date is not None \
                and promo_code.valid_end_date.replace(tzinfo=None) < datetime.utcnow():
            return Response(data='expired', status=status.HTTP_400_BAD_REQUEST)

        customer_promo_code.used = True
        customer_promo_code.transfer = validatorSerializer.validated_data.get('transfer', customer_promo_code.transfer)
        customer_promo_code.save()
        serializer = CustomerPromoCodeSerializer(customer_promo_code)
        return Response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.BasePermission],
            url_path='customer_promo_codes/(?P<customer_code>.*)')
    def customer_promo_codes(self, request, customer_code=None):
        try:
            customer_promo_codes = CustomerPromoCode.objects.filter(customer_code=customer_code)
        except:
            return Response(data='customer promo code not found', status=status.HTTP_404_NOT_FOUND)

        if customer_promo_codes.count() == 0:
            return Response(data='customer promo code not found', status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerPromoCodeListSerializer(customer_promo_codes, many=True, context={'request': request})

        return Response(serializer.data)
