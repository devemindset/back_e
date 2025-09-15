from rest_framework import serializers
from .models import Cart,CartItem
from products.serializers import ProductCategorySerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer(read_only=True)
    

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_category', 'quantity',]

class CreateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['cart', 'product_category', 'quantity',]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'items', 'created_at']

