from django.test import TestCase
from store.models import User, Product, Category, Vendor, Order, Cart, ProductVariant
from store.serializers import (
    UserSerializer, ProductSerializer, CategorySerializer, 
    OrderSerializer, CartSerializer
)


class UserSerializerTestCase(TestCase):
    """Test User serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            full_name="Test User",
            phone="1234567890"
        )

    def test_user_serializer_valid_data(self):
        """Serializer correctly serializes valid user data"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], "test@example.com")
        self.assertEqual(data['full_name'], "Test User")
        self.assertEqual(data['phone'], "1234567890")

    def test_user_serializer_has_required_fields(self):
        """Serializer includes required fields"""
        serializer = UserSerializer(self.user)
        self.assertIn('id', serializer.data)
        self.assertIn('email', serializer.data)
        self.assertIn('full_name', serializer.data)


class ProductSerializerTestCase(TestCase):
    """Test Product serializer"""

    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", slug="test-vendor")
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            category=self.category,
            vendor=self.vendor
        )

    def test_product_serializer_valid_data(self):
        """Serializer correctly serializes valid product data"""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data['name'], "Test Product")
        self.assertEqual(float(data['price']), 100.00)
        self.assertEqual(data['currency'], "USD")

    def test_product_serializer_includes_variants(self):
        """Serializer includes product variants"""
        variant = ProductVariant.objects.create(
            product=self.product,
            sku="VAR001",
            price=95.00
        )
        serializer = ProductSerializer(self.product)
        self.assertIn('variants', serializer.data)

    def test_product_serializer_validation(self):
        """Serializer validates required fields"""
        data = {
            "name": "",  # Empty name should fail
            "slug": "test",
            "price": 100.00
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class CategorySerializerTestCase(TestCase):
    """Test Category serializer"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_category_serializer_valid_data(self):
        """Serializer correctly serializes category data"""
        serializer = CategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data['name'], "Electronics")
        self.assertEqual(data['slug'], "electronics")

    def test_category_serializer_with_parent(self):
        """Serializer handles parent category"""
        parent = Category.objects.create(name="Tech", slug="tech")
        child = Category.objects.create(
            name="Computers",
            slug="computers",
            parent=parent
        )
        serializer = CategorySerializer(child)
        data = serializer.data
        self.assertIsNotNone(data['parent'])


class OrderSerializerTestCase(TestCase):
    """Test Order serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00,
            status="pending"
        )

    def test_order_serializer_valid_data(self):
        """Serializer correctly serializes order data"""
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(data['order_number'], "ORD001")
        self.assertEqual(float(data['total_amount']), 100.00)
        self.assertEqual(data['status'], "pending")

    def test_order_serializer_includes_user_and_items(self):
        """Serializer includes user and order items"""
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertIn('user', data)
        self.assertIn('items', data)


class CartSerializerTestCase(TestCase):
    """Test Cart serializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_serializer_valid_data(self):
        """Serializer correctly serializes cart data"""
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(str(data['user']), str(self.user.id))

    def test_cart_serializer_includes_items(self):
        """Serializer includes cart items"""
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertIn('items', data)
