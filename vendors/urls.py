from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vendors.views import UserRegistrationAPIView, VendorViewSet
from vendors.views import PurchaseOrderViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('register/', UserRegistrationAPIView.as_view(), name='user_registration'),
]
