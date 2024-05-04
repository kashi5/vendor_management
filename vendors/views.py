from django.utils import timezone
from rest_framework import viewsets
from vendors import serializers
from vendors.models import PurchaseOrder, Vendor, VendorMetrics, VendorPerformance
from vendors.serializers import (
    PurchaseOrderAcknowledgeSerializer,
    PurchaseOrderSerializer,
    VendorPerformaceSerializer,
    VendorSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema,OpenApiResponse
from rest_framework.authtoken.views import obtain_auth_token


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "Username for the new user",
                    "required": True,
                },
                "password": {
                    "type": "string",
                    "description": "Password for the new user",
                    "required": True,
                },
            },
        }
    }
)
class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "Username for the user",
                    "required": True,
                },
                "password": {
                    "type": "string",
                    "description": "Password for the user",
                    "required": True,
                },
            },
        }
    },
    responses={
        200: OpenApiResponse(
            response={"token": "string"},
            description="Authentication token for the user",
        )
    },
)
class ObtainAuthTokenView(APIView):
    def post(self, request):
        return obtain_auth_token(request._request)
    


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        vendor_id = self.request.query_params.get("vendor_id")
        if vendor_id:
            self.queryset = self.queryset.filter(vendor=vendor_id)
        return self.queryset


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Then save the instance
        serializer.save()
        vendor_obj = Vendor.objects.get(id=serializer.data["vendor_id"])

        # Vendor logic for metrics
        try:
            # Update the fulfillmate rate of the vendor when new order is taken and total orders in vendor metrics
            vendor_metric_obj = VendorMetrics.objects.get(vendor_id=vendor_obj)
            vendor_metric_obj.total_orders = vendor_metric_obj.total_orders + 1
            vendor_metric_obj.save()
            vendor_metric_obj = VendorMetrics.objects.get(vendor_id=vendor_obj)
            vendor_obj.fulfillment_rate = round(
                vendor_metric_obj.completed_orders
                / vendor_metric_obj.total_orders
                * 100,
                2,
            )
            vendor_obj.save()
        except VendorMetrics.DoesNotExist:
            VendorMetrics.objects.create(vendor_id=vendor_obj, total_orders=1)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        if (
            serializer.validated_data["status"] == "Completed"
            and serializer.validated_data["quality_rating"] is None
            or not instance.acknowledgement_date
        ):
            return Response(
                {"error": "Quality rating and acknowledge date  is required for completed orders"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        po_obj = serializer.save()
        vendor_obj = po_obj.vendor_id
        vendor_metric_obj = VendorMetrics.objects.get(vendor_id=vendor_obj)
        if po_obj.status == "completed":
            
            on_time_result = (
                1 if po_obj.delivery_date.date() >= po_obj.delivered_date.date() else 0
            )
            vendor_metric_obj.completed_orders = vendor_metric_obj.completed_orders + 1
            vendor_metric_obj.quality_rating_count = round(
                vendor_metric_obj.quality_rating_count + po_obj.quality_rating, 2
            )
            vendor_metric_obj.on_time_delivery_count = round(
                vendor_metric_obj.on_time_delivery_count + on_time_result, 2
            )
            vendor_metric_obj.save()

            vendor_obj.quality_rating_avg = (
                vendor_metric_obj.quality_rating_count
                / vendor_metric_obj.completed_orders
            )
            vendor_obj.fulfillment_rate = round(
                vendor_metric_obj.completed_orders
                / vendor_metric_obj.total_orders
                * 100,
                2,
            )
            vendor_obj.on_time_delivery_rate = round(
                vendor_metric_obj.on_time_delivery_count
                / vendor_metric_obj.completed_orders
                * 100,
                2,
            )
            vendor_obj.save()
        return Response(serializer.data)


class VendorPerformanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None, vendor_id=None):
        try:
            instance = Vendor.objects.get(id=vendor_id)
            serializer = VendorPerformaceSerializer(instance)
            return Response(serializer.data)
        except VendorPerformance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class PurchaseOrderAcknowledgeViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderAcknowledgeSerializer  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            po_obj = PurchaseOrder.objects.get(id=kwargs["id"])
            if not po_obj.acknowledgement_date:
                po_obj.acknowledgement_date = timezone.now()
                po_obj.save()
                vendor_obj = po_obj.vendor_id
                vendor_metric_obj = VendorMetrics.objects.get(vendor_id=vendor_obj)
                result = po_obj.acknowledgement_date - po_obj.issue_date
                time_result = round(result.total_seconds() / 3600, 2)
                
                vendor_metric_obj.total_acknowledgement_count = (
                    vendor_metric_obj.total_acknowledgement_count + 1
                )
                vendor_metric_obj.total_acknowledgement_rate = round(
                    vendor_metric_obj.total_acknowledgement_rate + time_result, 2
                )
                vendor_metric_obj.save()

                vendor_obj.average_response_time = round(
                    vendor_metric_obj.total_acknowledgement_rate
                    / vendor_metric_obj.total_orders,
                    2,
                )
                vendor_obj.save()
            serializer = PurchaseOrderAcknowledgeSerializer(po_obj)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response("Purchase order not avaialable",status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)