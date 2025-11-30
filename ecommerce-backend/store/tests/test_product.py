from rest_framework.test import APITestCase
from store.models import Product, Category

class ProductTests(APITestCase):
    def setUp(self):
        cat = Category.objects.create(name="c1", slug="c1")
        Product.objects.create(name="p1", slug="p1", price=5.00, currency="USD", category=cat)

    def test_list_products(self):
        resp = self.client.get("/api/products/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("results" in resp.data)
