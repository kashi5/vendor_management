# Generated by Django 5.0.4 on 2024-05-02 04:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=80)),
                ("contact_details", models.TextField()),
                ("address", models.TextField()),
                ("vendor_code", models.CharField(max_length=80, unique=True)),
                ("on_time_delivery_rate", models.FloatField(default=0.0)),
                ("quality_rating_avg", models.FloatField(default=0.0)),
                ("average_response_time", models.FloatField(default=0.0)),
                ("fulfillment_rate", models.FloatField(default=0.0)),
            ],
            options={
                "db_table": "vendor",
            },
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("items", models.JSONField()),
                ("quantity", models.IntegerField()),
                ("status", models.CharField(max_length=80)),
                ("order_date", models.DateTimeField()),
                ("delivery_date", models.DateTimeField()),
                ("delivered_date", models.DateTimeField()),
                ("issue_date", models.DateTimeField()),
                ("acknowledgement_date", models.DateTimeField(null=True)),
                ("quality_rating", models.FloatField(null=True)),
                (
                    "vendor_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vendors.vendor"
                    ),
                ),
            ],
            options={
                "db_table": "purchase_order",
            },
        ),
        migrations.CreateModel(
            name="VendorPerformance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("on_time_delivery_rate", models.FloatField()),
                ("quality_rating_avg", models.FloatField()),
                ("average_response_time", models.FloatField()),
                ("fulfillment_rate", models.FloatField()),
                (
                    "vendor_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vendors.vendor"
                    ),
                ),
            ],
            options={
                "db_table": "vendor_performance",
            },
        ),
    ]
