from rest_framework import serializers
from .models import User, Product, ProductVariant, Category, Cart, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email","full_name","phone")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id","name","slug","parent")

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("id","sku","attributes","price")

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ("id","vendor","category","name","slug","sku","price","currency","is_active","variants")

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id","variant","quantity","price_at_added")

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ("id","user","session_id","items")

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id","variant","quantity","unit_price","total_price")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id","order_number","user","total_amount","status","placed_at","items")
