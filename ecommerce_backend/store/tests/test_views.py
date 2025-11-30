from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from store.models import User, Product, Category, Vendor, Cart, CartItem, ProductVariant, Order
from store.serializers import (
    ProductSerializer, CategorySerializer, CartSerializer, 
    OrderSerializer, UserSerializer
)


class ProductAPITestCase(TestCase):
    """Test Product API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", slug="test-vendor")
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.vendor_user = User.objects.create_user(
            email="vendor@example.com",
            password="testpass123",
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            is_staff=False
        )

    def test_list_products_unauthenticated(self):
        """Anyone can list products"""
        Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            category=self.category,
            vendor=self.vendor
        )
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product_as_vendor(self):
        """Vendors can create products"""
        self.client.force_authenticate(user=self.vendor_user)
        data = {
            "name": "New Product",
            "slug": "new-product",
            "price": 50.00,
            "category": self.category.id,
            "vendor": self.vendor.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_regular_user_denied(self):
        """Regular users cannot create products"""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            "name": "New Product",
            "slug": "new-product",
            "price": 50.00,
            "category": self.category.id,
            "vendor": self.vendor.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_products_by_category(self):
        """Can filter products by category"""
        Product.objects.create(
            name="Electronics Product",
            slug="electronics-product",
            price=100.00,
            category=self.category,
            vendor=self.vendor
        )
        response = self.client.get(f'/api/products/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_products_by_name(self):
        """Can search products by name"""
        Product.objects.create(
            name="Laptop Pro",
            slug="laptop-pro",
            price=1000.00,
            category=self.category,
            vendor=self.vendor
        )
        response = self.client.get('/api/products/?search=Laptop')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_order_products_by_price(self):
        """Can order products by price"""
        Product.objects.create(
            name="Cheap Item",
            slug="cheap-item",
            price=10.00,
            category=self.category,
            vendor=self.vendor
        )
        Product.objects.create(
            name="Expensive Item",
            slug="expensive-item",
            price=1000.00,
            category=self.category,
            vendor=self.vendor
        )
        response = self.client.get('/api/products/?ordering=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertTrue(results[0]['price'] <= results[1]['price'])


class CartAPITestCase(TestCase):
    """Test Cart API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_user_can_see_own_cart(self):
        """Authenticated user can see their own cart"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/carts/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_other_carts(self):
        """User cannot see other users' carts"""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123"
        )
        other_cart = Cart.objects.create(user=other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/carts/{other_cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderAPITestCase(TestCase):
    """Test Order API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.vendor = Vendor.objects.create(name="Test Vendor", slug="test-vendor")
        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00,
            status="pending"
        )

    def test_user_can_see_own_order(self):
        """Authenticated user can see their own order"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_see_other_orders(self):
        """User cannot see other users' orders"""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123"
        )
        other_order = Order.objects.create(
            user=other_user,
            order_number="ORD002",
            total_amount=50.00,
            status="pending"
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/orders/{other_order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_see_all_orders(self):
        """Admin user can see all orders"""
        admin_user = User.objects.create_user(
            email="admin@example.com",
            password="testpass123",
            is_staff=True
        )
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123"
        )
        other_order = Order.objects.create(
            user=other_user,
            order_number="ORD002",
            total_amount=50.00,
            status="pending"
        )
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(f'/api/orders/{other_order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryAPITestCase(TestCase):
    """Test Category API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.vendor_user = User.objects.create_user(
            email="vendor@example.com",
            password="testpass123",
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            is_staff=False
        )

    def test_list_categories_unauthenticated(self):
        """Anyone can list categories"""
        Category.objects.create(name="Electronics", slug="electronics")
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_as_vendor(self):
        """Vendors can create categories"""
        self.client.force_authenticate(user=self.vendor_user)
        data = {"name": "New Category", "slug": "new-category"}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_regular_user_denied(self):
        """Regular users cannot create categories"""
        self.client.force_authenticate(user=self.regular_user)
        data = {"name": "New Category", "slug": "new-category"}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
