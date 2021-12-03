from django.urls import include, path
from rest_framework import routers
from emqapi.api.views import views, customer_promo_code, promo_code
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'promo-code', promo_code.PromoCodeViewSet)
router.register(r'customer-promo-code', customer_promo_code.CustomerPromoCodeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('spec', schema_view)
]
