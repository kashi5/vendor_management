from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vendors.views import (
    UserRegistrationAPIView,
    VendorPerformanceViewSet,
    VendorViewSet,
)
from vendors.views import PurchaseOrderViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"vendors", VendorViewSet)
router.register(r"purchase_orders", PurchaseOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "vendors/<uuid:vendor>/performance/",
        VendorPerformanceViewSet.as_view({"get": "retrieve"}),
        name="vendor-performance-detail",
    ),
    path("token/", obtain_auth_token, name="api_token_auth"),
    path("register/", UserRegistrationAPIView.as_view(), name="user_registration"),
]
