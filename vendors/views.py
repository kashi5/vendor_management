from rest_framework import viewsets
from vendors import serializers
from vendors.models import PurchaseOrder, Vendor, VendorMetrics, VendorPerformance
from vendors.serializers import (
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
from rest_framework.filters import SearchFilter

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


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            self.queryset = self.queryset.filter(vendor=vendor_id)
        return self.queryset
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Then save the instance
        serializer.save()
        vendor_obj = Vendor.objects.get(id=serializer.data["vendor"])

        # Vendor logic for metrics
        try:
            # Update the fulfillmate rate of the vendor when new order is taken and total orders in vendor metrics 
            vendor_metric_obj = VendorMetrics.objects.get(vendor=vendor_obj)
            vendor_metric_obj.total_orders = vendor_metric_obj.total_orders + 1
            vendor_metric_obj.save()
            vendor_metric_obj = VendorMetrics.objects.get(vendor=vendor_obj)
            vendor_obj.update(fulfillment_rate=vendor_metric_obj.completed_orders/vendor_metric_obj.total_orders * 100)
        except VendorMetrics.DoesNotExist:
            VendorMetrics.objects.create(vendor=vendor_obj, total_orders=1)
        


        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        if (
            serializer.validated_data["status"] == "Completed"
            and serializer.validated_data["quality_rating"] is None
        ):
            raise serializer.ValidationError(
                "Quality rating is required for completed orders"
            )

        po_obj = serializer.save()
        if po_obj.status == "completed":
            vendor_obj = po_obj.vendor
            vendor_metric_obj = VendorMetrics.objects.get(vendor=vendor_obj)
            on_time_result = 1 if po_obj.delivery_date.date()>= po_obj.delivered_date.date() else 0
            vendor_metric_obj.completed_orders = vendor_metric_obj.completed_orders + 1
            vendor_metric_obj.quality_rating_count = vendor_metric_obj.quality_rating_count + po_obj.quality_rating
            vendor_metric_obj.on_time_delivery_count = vendor_metric_obj.on_time_delivery_count + on_time_result
            vendor_metric_obj.save()
            
            vendor_obj.quality_rating_avg=vendor_metric_obj.quality_rating_count/ vendor_metric_obj.completed_orders
            vendor_obj.fulfillment_rate=vendor_metric_obj.completed_orders/vendor_metric_obj.total_orders * 100
            vendor_obj.on_time_delivery_rate = vendor_metric_obj.on_time_delivery_count/vendor_metric_obj.completed_orders * 100
            vendor_obj.save()

        elif po_obj.acknowledgement_date:
            result = po_obj.acknowledgement_date  - po_obj.issue_date
            time_result = round(result.total_seconds() / 3600, 2)
            vendor_obj =po_obj.vendor
            vendor_metric_obj = VendorMetrics.objects.get(vendor=vendor_obj)
            vendor_metric_obj.total_acknowledgement_count =vendor_metric_obj.total_acknowledgement_count + 1
            vendor_metric_obj.total_acknowledgement_rate = vendor_metric_obj.total_acknowledgement_rate + time_result
            vendor_metric_obj.save()    
            # vendor_metric_obj = VendorMetrics.objects.get(vendor=vendor_obj)
            vendor_obj.average_response_time=vendor_metric_obj.total_acknowledgement_rate/vendor_metric_obj.total_orders
            vendor_obj.save()           
        return Response(serializer.data)


class VendorPerformanceViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None, vendor=None):
        try:
            instance = Vendor.objects.get(id=vendor)
            serializer = VendorPerformaceSerializer(instance)
            return Response(serializer.data)
        except VendorPerformance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
