from rest_framework import viewsets
from vendors.models import PurchaseOrder, Vendor, VendorMetrics, VendorPerformance
from vendors.serializers import PurchaseOrderSerializer, VendorPerformaceSerializer, VendorSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)



class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Then save the instance
        serializer.save()
        vendor_obj = Vendor.objects.get(id=serializer.data['vendor_id'])

        #Vendor logic for metrics
        try:
           vendor_metric_obj= VendorMetrics.objects.get(vendor_id=vendor_obj)
           vendor_metric_obj.total_orders=vendor_metric_obj.total_orders+1
           vendor_metric_obj.save()
        except VendorMetrics.DoesNotExist:
            VendorMetrics.objects.create(vendor_id=vendor_obj,total_orders=1)

        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        # Add your custom logic here before saving the instance
        # For example, you can access request.data and perform calculations or validations
        # Then save the instance
        serializer.save()
        return Response(serializer.data)


class VendorPerformanceViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None, vendor_id=None):
        try:
            instance = Vendor.objects.get(id=vendor_id)
            serializer = VendorPerformaceSerializer(instance)
            return Response(serializer.data)
        except VendorPerformance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
