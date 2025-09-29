from rest_framework import serializers
from .models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'email', 'address', 'total_amount', 'status', 'items', 'created_at',"session_id"]

class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'full_name', 'email', 'address',"session_id",'total_amount','phonenumber',"items",]