from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    message = "Only admin users are allowed to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsVendor(permissions.BasePermission):
    """
    Allows access only to vendor users (staff users who manage products).
    """
    message = "Only vendors are allowed to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        # Only allow vendor to edit their own products
        if hasattr(obj, 'vendor') and hasattr(obj.vendor, 'contact_email'):
            return request.user and request.user.email == obj.vendor.contact_email
        return False


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Allows vendors to edit products, anyone can read.
    """
    message = "Only vendors can edit products. Read-only access for others."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Vendor can only edit their own products
        if hasattr(obj, 'vendor') and hasattr(obj.vendor, 'contact_email'):
            return request.user and request.user.email == obj.vendor.contact_email
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows users to edit their own objects or admins can edit any object.
    """
    message = "You can only edit your own objects."

    def has_object_permission(self, request, view, obj):
        # Admin can edit anything
        if request.user and request.user.is_staff:
            return True
        # Users can edit their own objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class IsOwner(permissions.BasePermission):
    """
    Allows users to access only their own objects.
    """
    message = "You can only access your own objects."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
