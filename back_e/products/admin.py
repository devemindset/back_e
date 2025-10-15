from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product,
    ProductCategory,
    ProductImage,
    ProductTestimonials,
    ProductLandingImage,
    ProductLandingVideo,
    ProductVideo,
    ProductImageLand,
    TestimonialDetail
)

# -----------------------------
# 🔹 Product
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "description",)
    search_fields = ("name", "description")


# -----------------------------
# 🔹 Product Category
# -----------------------------
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("product", "category_name", "description", "colors", "weight_gram", "sizes",)
    search_fields = ("category_name", "product__name")
    list_filter = ("colors", "sizes")


# -----------------------------
# 🔹 Product Image (avec aperçu)
# -----------------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product_category", "preview_image", "alt_text")
    search_fields = ("product_category__category_name", "alt_text")

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:6px;"/>', obj.image.url)
        return "-"
    preview_image.short_description = "Aperçu"


# -----------------------------
# 🔹 Product Video (avec aperçu)
# -----------------------------
@admin.register(ProductVideo)
class ProductVideoAdmin(admin.ModelAdmin):
    list_display = ("name", "preview_video", "created_at", "updated_at",)
    search_fields = ("name",)
    readonly_fields = ("preview_video",)

    def preview_video(self, obj):
        if obj.video:
            return format_html(
                '<video width="220" height="160" controls>'
                '<source src="{}" type="video/mp4">'
                '</video>',
                obj.video.url
            )
        return "-"
    preview_video.short_description = "Aperçu vidéo"


# -----------------------------
# 🔹 Product Image Land (avec aperçu)
# -----------------------------
@admin.register(ProductImageLand)
class ProductImageLandAdmin(admin.ModelAdmin):
    list_display = ("name","title","description", "preview_image", "created_at", "updated_at",)
    search_fields = ("name",)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:6px;"/>', obj.image.url)
        return "-"
    preview_image.short_description = "Aperçu"


# -----------------------------
# 🔹 Product Landing Video
# -----------------------------
@admin.register(ProductLandingVideo)
class ProductLandingVideoAdmin(admin.ModelAdmin):
    list_display = ("product_category", "video_category", "title", "description", "created_at", "updated_at",)
    search_fields = ("title", "product_category__category_name", "video_category",)
    list_filter = ("video_category",)


# -----------------------------
# 🔹 Product Landing Image (avec aperçu)
# -----------------------------
@admin.register(ProductLandingImage)
class ProductLandingImageAdmin(admin.ModelAdmin):
    list_display = ("product_category", "image_category_land",)
    search_fields = ("image_category_land",)



# -----------------------------
# 🔹 Testimonial Detail
# -----------------------------
@admin.register(TestimonialDetail)
class TestimonialDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "product_name","preview_image",)
    search_fields = ("name", "product_name")

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:6px;"/>', obj.image.url)
        return "-"
    preview_image.short_description = "Aperçu"


# -----------------------------
# 🔹 Product Testimonials
# -----------------------------
@admin.register(ProductTestimonials)
class ProductTestimonialsAdmin(admin.ModelAdmin):
    list_display = ("product_category", "testimonial",)
    search_fields = ("product_category__category_name", "testimonial__name")
