from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Cart, Order
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from .chapa.client import ChapaClient

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "vendor", "is_active"]
    search_fields = ["name","slug","sku"]
    ordering_fields = ["price","created_at"]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def pay(self, request, pk=None):
        order = self.get_object()
        client = ChapaClient()
        # initiate payment and return url (minimal example)
        data = client.create_payment(order.order_number, float(order.total_amount))
        return Response({"payment": data})
