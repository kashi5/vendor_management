import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
"""This model is used to store the Vendor Details"""


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=80, blank=False, null=False)
    contact_details = models.TextField(blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    vendor_code = models.CharField(max_length=80, blank=False, null=False, unique=True)
    on_time_delivery_rate = models.FloatField(blank=False, null=False, default=0.0)
    quality_rating_avg = models.FloatField(blank=False, null=False, default=0.0)
    average_response_time = models.FloatField(blank=False, null=False, default=0.0)
    fulfillment_rate = models.FloatField(blank=False, null=False, default=0.0)

    class Meta:
        db_table = "vendor"

    def add_vendor_performance(self):
        VendorPerformance.objects.create(
            vendor=self,
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate,
        )


"""This model is used to store the Order Details"""


class PurchaseOrder(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, blank=False, null=False, on_delete=models.CASCADE
    )
    items = models.JSONField(blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    status = models.CharField(
        max_length=80, blank=False, null=False, choices=STATUS_CHOICES
    )
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    delivered_date = models.DateTimeField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgement_date = models.DateTimeField(null=True)
    quality_rating = models.FloatField(null=True)

    class Meta:
        db_table = "purchase_order"


"""This model is used to store the Vendor Metrics"""


class VendorMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, blank=False, null=False, on_delete=models.CASCADE
    )
    completed_orders = models.IntegerField(blank=False, null=False, default=0)
    total_orders = models.IntegerField(blank=False, null=False, default=0)
    quality_rating_count = models.IntegerField(blank=False, null=False, default=0)
    total_acknowledgement_count = models.IntegerField(blank=False, null=False, default=0)
    total_acknowledgement_rate  = models.FloatField(blank=False, null=False, default=0.0)
    on_time_delivery_count = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = "vendor_metrics"


"""This model is used to store the Performance Details"""


class VendorPerformance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, blank=False, null=False, on_delete=models.CASCADE
    )
    on_time_delivery_rate = models.FloatField(blank=False, null=False)
    quality_rating_avg = models.FloatField(blank=False, null=False)
    average_response_time = models.FloatField(blank=False, null=False)
    fulfillment_rate = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = "vendor_performance"


# Model Signals for Vendor Model
@receiver(post_save, sender=Vendor)
def update_vendor_performance(sender, instance, created, **kwargs):
    if created:
        instance.add_vendor_performance()
    else:
        print("Updating Vendor Performance")
        VendorPerformance.objects.create(
            vendor= instance,
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfillment_rate=instance.fulfillment_rate)
