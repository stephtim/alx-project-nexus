from django.test import TestCase
from store.models import (
    User, Product, Category, Vendor, Cart, CartItem, Order, OrderItem,
    ProductVariant, Address, Role, UserRole, Coupon, Review, Payment, Notification
)
import uuid


class UserModelTestCase(TestCase):
    """Test User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            full_name="Test User"
        )

    def test_user_creation(self):
        """User is created successfully"""
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.full_name, "Test User")

    def test_user_has_uuid_pk(self):
        """User has UUID primary key"""
        self.assertIsInstance(self.user.id, uuid.UUID)

    def test_user_email_is_unique(self):
        """User email must be unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test@example.com",
                password="testpass123"
            )

    def test_user_authentication(self):
        """User can authenticate"""
        user = User.objects.get(email="test@example.com")
        self.assertTrue(user.check_password("testpass123"))


class ProductModelTestCase(TestCase):
    """Test Product model"""

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

    def test_product_creation(self):
        """Product is created successfully"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(self.product.price, 100.00)

    def test_product_has_uuid_pk(self):
        """Product has UUID primary key"""
        self.assertIsInstance(self.product.id, uuid.UUID)

    def test_product_slug_is_unique(self):
        """Product slug must be unique"""
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Another Product",
                slug="test-product",
                price=50.00
            )

    def test_product_default_currency(self):
        """Product has default currency USD"""
        self.assertEqual(self.product.currency, "USD")

    def test_product_active_by_default(self):
        """Product is active by default"""
        self.assertTrue(self.product.is_active)


class CategoryModelTestCase(TestCase):
    """Test Category model"""

    def test_category_creation(self):
        """Category is created successfully"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.slug, "electronics")

    def test_category_hierarchy(self):
        """Category can have parent category"""
        parent = Category.objects.create(name="Tech", slug="tech")
        child = Category.objects.create(
            name="Computers",
            slug="computers",
            parent=parent
        )
        self.assertEqual(child.parent, parent)

    def test_category_slug_is_unique(self):
        """Category slug must be unique"""
        Category.objects.create(name="Electronics", slug="electronics")
        with self.assertRaises(Exception):
            Category.objects.create(name="Other Electronics", slug="electronics")


class VendorModelTestCase(TestCase):
    """Test Vendor model"""

    def test_vendor_creation(self):
        """Vendor is created successfully"""
        vendor = Vendor.objects.create(
            name="Test Vendor",
            slug="test-vendor",
            contact_email="vendor@example.com"
        )
        self.assertEqual(vendor.name, "Test Vendor")
        self.assertEqual(vendor.slug, "test-vendor")


class OrderModelTestCase(TestCase):
    """Test Order model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_order_creation(self):
        """Order is created successfully"""
        order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00,
            status="pending"
        )
        self.assertEqual(order.order_number, "ORD001")
        self.assertEqual(order.status, "pending")

    def test_order_has_uuid_pk(self):
        """Order has UUID primary key"""
        order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00
        )
        self.assertIsInstance(order.id, uuid.UUID)

    def test_order_has_placed_at_timestamp(self):
        """Order has placed_at timestamp"""
        order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00
        )
        self.assertIsNotNone(order.placed_at)


class CartModelTestCase(TestCase):
    """Test Cart model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_cart_creation(self):
        """Cart is created successfully"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)

    def test_cart_has_uuid_pk(self):
        """Cart has UUID primary key"""
        cart = Cart.objects.create(user=self.user)
        self.assertIsInstance(cart.id, uuid.UUID)


class AddressModelTestCase(TestCase):
    """Test Address model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_address_creation(self):
        """Address is created successfully"""
        address = Address.objects.create(
            user=self.user,
            recipient_name="John Doe",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        self.assertEqual(address.recipient_name, "John Doe")
        self.assertEqual(address.city, "New York")

    def test_address_related_to_user(self):
        """Address is related to user"""
        address = Address.objects.create(
            user=self.user,
            recipient_name="John Doe",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        self.assertEqual(address.user, self.user)


class ReviewModelTestCase(TestCase):
    """Test Review model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.vendor = Vendor.objects.create(name="Test Vendor", slug="test-vendor")
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            category=self.category,
            vendor=self.vendor
        )

    def test_review_creation(self):
        """Review is created successfully"""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Great Product"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, "Great Product")

    def test_review_verified_purchase_default(self):
        """Review has is_verified_purchase flag"""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5
        )
        self.assertFalse(review.is_verified_purchase)


class PaymentModelTestCase(TestCase):
    """Test Payment model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD001",
            total_amount=100.00
        )

    def test_payment_creation(self):
        """Payment is created successfully"""
        payment = Payment.objects.create(
            order=self.order,
            payment_provider="chapa",
            amount=100.00,
            status="pending"
        )
        self.assertEqual(payment.status, "pending")
        self.assertEqual(payment.payment_provider, "chapa")


class NotificationModelTestCase(TestCase):
    """Test Notification model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_notification_creation(self):
        """Notification is created successfully"""
        notification = Notification.objects.create(
            user=self.user,
            type="order_placed",
            payload={"order_id": "ORD001"}
        )
        self.assertEqual(notification.type, "order_placed")
        self.assertFalse(notification.is_read)
