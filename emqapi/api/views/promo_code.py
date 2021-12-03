from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from emqapi.api.serializers import PromoCodeSerializer
from emqapi.api.models import PromoCode


class PromoCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.BasePermission]

    @action(detail=True, methods=['put'], permission_classes=[permissions.BasePermission])
    def update_promo_code_enable(self, request, pk=None):
        promo_code = PromoCode.objects.get(code=pk)
        promo_code.enable = not promo_code.enable
        promo_code.save()
        serializer = PromoCodeSerializer(promo_code)
        return Response(serializer.data)