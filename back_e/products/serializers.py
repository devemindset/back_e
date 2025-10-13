from rest_framework import serializers
from .models import (
    Product,
    ProductCategory,
    ProductImage,
    ProductLandingImage,
    ProductLandingVideo,
    ProductTestimonials,
    ProductVideo,
    ProductImageLand,
    TestimonialDetail
)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'product_category']


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['video']


class ProductImageLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageLand
        fields = ['id', 'name', 'image', 'title', 'description', 'created_at']


class ProductCategoryLandingVideoSerializer(serializers.ModelSerializer):
    video = ProductVideoSerializer(read_only=True, source="video_category")

    class Meta:
        model = ProductLandingVideo
        fields = ["video", "title", "description"]


class ProductCategoryLandingImageSerializer(serializers.ModelSerializer):
    image_category_land = ProductImageLandSerializer(read_only=True)

    class Meta:
        model = ProductLandingImage
        fields = ['id', 'image_category_land', 'created_at']


class TestimonialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialDetail
        fields = ["image", "name", "description"]


class ProductCategoryLandingTestimonials(serializers.ModelSerializer):
    testimonial = TestimonialDetailSerializer(read_only=True)

    class Meta:
        model = ProductTestimonials
        fields = ["testimonial"]


class ProductCategorySerializer(serializers.ModelSerializer):
    images_detail = ProductImageSerializer(many=True, read_only=True, source='category_images')
    landing_video = ProductCategoryLandingVideoSerializer(many=True, read_only=True, source="category_video_landing")
    category_image_landing = ProductCategoryLandingImageSerializer(many=True, read_only=True)
    landing_testimonials = ProductCategoryLandingTestimonials(many=True, read_only=True, source="category_testimonial_landing")

    class Meta:
        model = ProductCategory
        fields = [
            'id', 'category_name', 'description', 'slug',
            'images_detail', 'created_at', 'updated_at',
            "price", "size", "color", "weight_grams", "currencyCode",
            "landing_video", 'category_image_landing', "landing_testimonials","same_category_name"
        ]


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
