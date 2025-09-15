from rest_framework import serializers
from .models import Product,ProductCategory,ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text','product_category',]

class ProductCategorySerializer(serializers.ModelSerializer):
    images_detail = ProductImageSerializer(many=True, read_only=True, source='category_images')
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'description', 'slug', 'images_detail', 'created_at', 'updated_at',"price","currencyCode"]

class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"

