from django.test import TestCase
from rest_framework.test import APIRequestFactory
from store.models import User, Product, Category, Vendor
from store.permissions import IsVendor, IsVendorOrReadOnly, IsOwnerOrAdmin, IsOwner, IsAdmin


class PermissionsTestCase(TestCase):
    """Test custom permission classes"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="testpass123",
            is_staff=True
        )
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
        self.vendor = Vendor.objects.create(name="Test Vendor", slug="test-vendor")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            vendor=self.vendor
        )

    def test_is_admin_permission_allows_staff(self):
        """IsAdmin permission allows staff users"""
        permission = IsAdmin()
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))

    def test_is_admin_permission_denies_regular_user(self):
        """IsAdmin permission denies regular users"""
        permission = IsAdmin()
        request = self.factory.get('/')
        request.user = self.regular_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_vendor_or_readonly_allows_read_for_all(self):
        """IsVendorOrReadOnly allows read access for all users"""
        permission = IsVendorOrReadOnly()
        request = self.factory.get('/')
        request.user = self.regular_user
        self.assertTrue(permission.has_permission(request, None))

    def test_is_vendor_or_readonly_allows_write_for_vendors(self):
        """IsVendorOrReadOnly allows write access for vendors"""
        permission = IsVendorOrReadOnly()
        request = self.factory.post('/')
        request.user = self.vendor_user
        self.assertTrue(permission.has_permission(request, None))

    def test_is_vendor_or_readonly_denies_write_for_regular_user(self):
        """IsVendorOrReadOnly denies write access for regular users"""
        permission = IsVendorOrReadOnly()
        request = self.factory.post('/')
        request.user = self.regular_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_owner_or_admin_allows_admin(self):
        """IsOwnerOrAdmin allows admins to edit any object"""
        permission = IsOwnerOrAdmin()
        request = self.factory.patch('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_object_permission(request, None, self.product))

    def test_is_owner_allows_owner(self):
        """IsOwner allows owner to access their object"""
        permission = IsOwner()
        request = self.factory.get('/')
        request.user = self.regular_user
        # Create an object with user field
        order = type('Order', (), {'user': self.regular_user})()
        self.assertTrue(permission.has_object_permission(request, None, order))

    def test_is_owner_denies_non_owner(self):
        """IsOwner denies non-owner access"""
        permission = IsOwner()
        request = self.factory.get('/')
        request.user = self.regular_user
        # Create an object with different user
        order = type('Order', (), {'user': self.admin_user})()
        self.assertFalse(permission.has_object_permission(request, None, order))
