from django.contrib import admin
from .models import Product,ProductCategory,ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","description","stock",)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("product","category_name","description",)

@admin.register(ProductImage)
class ProductAdminImage(admin.ModelAdmin):
    list_display = ("product_category","image","alt_text")