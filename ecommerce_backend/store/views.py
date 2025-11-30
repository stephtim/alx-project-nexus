from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Cart, Order
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from .chapa.client import ChapaClient
from .permissions import IsVendorOrReadOnly, IsOwnerOrAdmin, IsOwner

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "vendor", "is_active"]
    search_fields = ["name","slug","sku"]
    ordering_fields = ["price","created_at"]
    permission_classes = [IsVendorOrReadOnly]

    def get_permissions(self):
        """
        Override permissions: POST/PUT/DELETE require vendor, GET is public
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsVendorOrReadOnly()]
        return [permissions.AllowAny()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrReadOnly]

    def get_permissions(self):
        """
        Override permissions: Only vendors can modify categories
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsVendorOrReadOnly()]
        return [permissions.AllowAny()]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Users can only see their own carts
        """
        user = self.request.user
        if user.is_staff:
            return Cart.objects.all()
        if user.is_authenticated:
            return Cart.objects.filter(user=user)
        return Cart.objects.none()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Users see only their own orders, admins see all orders
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    @action(detail=True, methods=["post"], permission_classes=[IsOwnerOrAdmin])
    def pay(self, request, pk=None):
        order = self.get_object()
        self.check_object_permissions(request, order)
        client = ChapaClient()
        try:
            data = client.create_payment(order.order_number, float(order.total_amount))
            return Response(
                {"success": True, "payment": data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
