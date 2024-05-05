from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from vendors.models import Vendor, PurchaseOrder, VendorMetrics, VendorPerformance

class TestVendorViewSet(APITestCase):
    url = "/api/vendors/"

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create a vendor
        self.vendor = Vendor.objects.create(name='ekart', contact_details="9888888888", address="ekart address", vendor_code="E1")
        self.vendor_e2 = Vendor.objects.create(name='mkart', contact_details="9888888888", address="ekart address", vendor_code="E2")
        # Get the authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        # Set the authentication credentials for the API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_vendors(self):
        response = self.client.get(self.url)
        result = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 4)
        self.assertEqual(result['results'][0]["name"], self.vendor.name)

    def test_post_vendor(self):
        data = {'name': 'New Vendor', 'contact_details': '1234567890', 'address': 'New Address', 'vendor_code': 'NV1'}
        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, 201)
        self.assertEqual(Vendor.objects.count(), 3)
    
    def test_get_vendor_detail(self):
        response = self.client.get(f"{self.url}{self.vendor.id}/")
        result = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], self.vendor.name)
    
    def test_put_vendor_detail(self):
        data = {'name':'mkart new', 'contact_details':"9888888888", 'address':"ekart address", 'vendor_code':"E2"}
        response = self.client.put(self.url + str(self.vendor_e2.id) + "/", data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Vendor.objects.count(), 2)
        self.assertEqual(Vendor.objects.get(id=self.vendor_e2.id).name, 'mkart new')

    def test_get_vendor_performance(self):
        # Create a vendor performance object for the vendor
        response = self.client.get(self.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(self.vendor.id))
        self.assertEqual(result["on_time_delivery_rate"], self.vendor.on_time_delivery_rate)
        self.assertEqual(result["quality_rating_avg"], self.vendor.quality_rating_avg)
        self.assertEqual(result["average_response_time"], self.vendor.average_response_time)
        self.assertEqual(result["fulfillment_rate"], self.vendor.fulfillment_rate)
    
    def test_delete_vendor(self):
        # Delete the vendor
        response = self.client.delete(self.url + str(self.vendor.id) + "/")
        self.assertEquals(response.status_code, 204)
        self.assertEqual(Vendor.objects.count(), 1)


class TestPurchaseOrderViewSet(APITestCase):
    url = "/api/purchase_orders/"

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")

        self.token = Token.objects.create(user=self.user)

        # Set the authentication credentials for the API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        # Create a vendor
        vendor_data = {'name': 'ekart', 'contact_details': '9888888888', 'address': 'ekart address','vendor_code': 'E1'}
        response = self.client.post("/api/vendors/", data=vendor_data)
        self.vendor = Vendor.objects.get(vendor_code='E1')

        vendor_data_e2 = {'name':'mkart', 'contact_details': '9888888881', 'address': 'mkart address','vendor_code': 'E2'}
        response = self.client.post("/api/vendors/", data=vendor_data_e2)
        self.vendor_e2 = Vendor.objects.get(vendor_code='E2')
        # Create a purchase order
        # Create purchase orders using the POST method
        purchase_order_data = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 10, "item2": 20},
            "quantity": 10,
            "status": "pending",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": None,
            "quality_rating": None
        }
        
        response = self.client.post(self.url, data=purchase_order_data, format='json')
        self.purchase_order1 = PurchaseOrder.objects.get(id=response.data['id'])

        purchase_order_data_e2 = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 11, "item2": 21},
            "quantity": 11,
            "status": "pending",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": None,
            "quality_rating": None
        }
        response = self.client.post(self.url, data=purchase_order_data_e2, format='json')
        self.purchase_order2 = PurchaseOrder.objects.get(id=response.data['id'])



        purchase_order_data_e3 = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 12, "item2": 22},
            "quantity": 12,
            "status": "pending",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": None,
            "quality_rating": None
        }
        response = self.client.post(self.url, data=purchase_order_data_e3, format='json')
        self.purchase_order3 = PurchaseOrder.objects.get(id=response.data['id'])



        purchase_order_data_e4 = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 13, "item2": 23},
            "quantity": 13,
            "status": "pending",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": None,
            "quality_rating": None
        }
        response = self.client.post(self.url, data=purchase_order_data_e4, format='json')
        self.purchase_order4 = PurchaseOrder.objects.get(id=response.data['id'])

        purchase_order_data5 ={
            "vendor_id": str(self.vendor_e2.id),
            "items": {"item1": 14, "item2": 24},
            "quantity": 14,
            "status": "pending",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": None,
            "quality_rating": None 
        }
        response = self.client.post(self.url, data=purchase_order_data5, format='json')
        self.purchase_order5 = PurchaseOrder.objects.get(id=response.data['id'])
  
        
    def test_1_get_purchase_orders(self):
        response = self.client.get(self.url)
        result = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['results'][0]["vendor_id"], str(self.vendor.id))
        self.assertEqual(result['results'][0]["status"], str(self.purchase_order1.status))


    def test_2_get_purchase_order_filterd_by_vendor_id(self):
        response = self.client.get(self.url + "?vendor_id=" + str(self.vendor_e2.id))
        result = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['count'], 1)

    def test_3_purchase_order_acknowledge_status_change_vendor_performance(self):
        data = {"acknowledgement_date": "2024-05-01T06:14:53.845Z"}
        response = self.client.patch(self.url + str(self.purchase_order1.id) + "/acknowledge/",data=data)
        result = response.json()

        self.purchase_order1.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],0.0)
        self.assertEqual(result["quality_rating_avg"],0.0)
        self.assertEqual(result["average_response_time"],2.31)
        self.assertEqual(result["fulfillment_rate"], 0.0)



        response = self.client.patch(self.url + str(self.purchase_order2.id) + "/acknowledge/",data=data)
        result = response.json()
        self.assertEquals(response.status_code, 200)

        self.purchase_order2.refresh_from_db()


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],0.0)
        self.assertEqual(result["quality_rating_avg"],0.0)
        self.assertEqual(result["average_response_time"],4.63)
        self.assertEqual(result["fulfillment_rate"], 0.0)

        response = self.client.patch(self.url + str(self.purchase_order3.id) + "/acknowledge/",data=data)
        result = response.json()
        self.assertEquals(response.status_code, 200)

        self.purchase_order3.refresh_from_db()


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],0.0)
        self.assertEqual(result["quality_rating_avg"],0.0)
        self.assertEqual(result["average_response_time"],6.95)
        self.assertEqual(result["fulfillment_rate"], 0.0)

        # Updating the status to complete


        data = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 10, "item2": 20},
            "quantity": 10,
            "status": "completed",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": "2024-05-02T20:59:00Z",
            "quality_rating": 3
        }


        response = self.client.put(self.url + str(self.purchase_order1.id) + "/",data=data,format='json')
        result = response.json()

        self.purchase_order1.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],100.0)
        self.assertEqual(result["quality_rating_avg"],3.0)
        self.assertEqual(result["average_response_time"],6.95)
        self.assertEqual(result["fulfillment_rate"], 25.0)


        data = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 10, "item2": 20},
            "quantity": 10,
            "status": "completed",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": "2024-05-02T20:59:00Z",
            "quality_rating": 4
        }

        response = self.client.put(self.url + str(self.purchase_order1.id) + "/",data=data,format='json')
        result = response.json()
        self.assertEquals(response.status_code, 200)

        self.purchase_order2.refresh_from_db()


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],100.0)
        self.assertEqual(result["quality_rating_avg"],3.5)
        self.assertEqual(result["average_response_time"],6.95)
        self.assertEqual(result["fulfillment_rate"], 50.0)


        data = {
            "vendor_id": str(self.vendor.id),
            "items": {"item1": 10, "item2": 20},
            "quantity": 10,
            "status": "completed",
            "order_date": "2024-04-29T20:59:00Z",
            "delivery_date": "2024-05-12T20:59:00Z",
            "issue_date": "2024-04-30T20:59:00Z",
            "delivered_date": "2024-05-22T20:59:00Z",
            "quality_rating": 5
        }

        response = self.client.put(self.url + str(self.purchase_order1.id) + "/",data=data,format='json')
        result = response.json()
        self.assertEquals(response.status_code, 200)

        self.purchase_order3.refresh_from_db()


        response = self.client.get(TestVendorViewSet.url + str(self.vendor.id) + "/performance/")
        result = response.json()
        self.vendor.refresh_from_db()
        vendor_obj = Vendor.objects.get(id=self.vendor.id)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], str(vendor_obj.id))
        self.assertEqual(result["on_time_delivery_rate"],66.67)
        self.assertEqual(result["quality_rating_avg"],4.0)
        self.assertEqual(result["average_response_time"],6.95)
        self.assertEqual(result["fulfillment_rate"], 75.0)

        