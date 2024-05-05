from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vendors.views import (
    ObtainAuthTokenView,
    PurchaseOrderAcknowledgeViewSet,
    UserRegistrationAPIView,
    VendorPerformanceViewSet,
    VendorViewSet,
)
from vendors.views import PurchaseOrderViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"vendors", VendorViewSet)
router.register(r"purchase_orders", PurchaseOrderViewSet, basename="purchase-order")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "vendors/<uuid:vendor_id>/performance/",
        VendorPerformanceViewSet.as_view({"get": "retrieve"}),
        name="vendor-performance-detail",
    ),
     path(
        "purchase_orders/<uuid:id>/acknowledge/",
        PurchaseOrderAcknowledgeViewSet.as_view({"patch": "partial_update"}),
        name="purchase-order-acknowledge",
    ),
    path("token/", ObtainAuthTokenView.as_view(), name="api_token_auth"),
    path("register/", UserRegistrationAPIView.as_view(), name="user_registration"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
