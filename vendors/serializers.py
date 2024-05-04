from rest_framework import serializers
from vendors.models import PurchaseOrder, Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        # exclude = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time','fulfillment_rate']


class VendorPerformaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','on_time_delivery_rate', 'quality_rating_avg', 'average_response_time','fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
