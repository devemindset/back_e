from rest_framework import serializers
from .models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderItemPostSerializer(serializers.Serializer):
    product_category = serializers.IntegerField()
    quantity = serializers.IntegerField()

class AddressSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=255)
    apartment = serializers.CharField(max_length=100, allow_blank=True, required=False)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, allow_blank=True, required=False)
    zip = serializers.CharField(max_length=20)

class OrderPostSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=Order._meta.get_field("user").remote_field.model.objects.all(),
        allow_null=True, required=False
    )
    session_id = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=False)
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phonenumber = serializers.CharField(max_length=255)
    address = AddressSerializer()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = OrderItemPostSerializer(many=True)