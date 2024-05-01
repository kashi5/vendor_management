
from django.urls import path

urlpatterns = [
    path('api/vendors', vendors_list, name="Vendors List"),
]