from django.db import models
from django.utils.text import slugify
import os 

def upload_cover(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/product_cover/{instance.name}_{clean_name}{ext.lower()}"


def upload_product_detail_cover(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/product_detail_cover/{instance.alt_text}_{clean_name}{ext.lower()}"

def upload_product_video_landing_page(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/product_video_landing_page/{instance.name}_{clean_name}{ext.lower()}"

def upload_product_image_landing_page(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/product_image_landing_page/{instance.name}_{clean_name}{ext.lower()}"

def upload_testimonial_landing_page(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/testimonial_landing_page/{instance.name}_{clean_name}{ext.lower()}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    colors = models.BooleanField(default=False)
    weight_gram = models.BooleanField(default=False)
    sizes = models.BooleanField(default=False)
    same_category_name = models.CharField(null=True,blank=True) # The same category name
    shipping_time_usa = models.CharField(max_length=15,null=True,blank=True)
    shipping_time_europe = models.CharField(max_length=15,null=True,blank=True)
    shipping_time_asia = models.CharField(max_length=15,null=True,blank=True)
    shipping_time_woldwide = models.CharField(max_length=15,null=True,blank=True)
    currencyCode = models.CharField(max_length=3,null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class ProductImage(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='category_images')
    image = models.ImageField(upload_to=upload_product_detail_cover)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = self.product_category.category_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.alt_text 


class ProductVideo(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    video = models.FileField(upload_to=upload_product_video_landing_page)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class ProductLandingVideo(models.Model):
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name="category_video_landing")
    video_category = models.ForeignKey(ProductVideo,on_delete=models.CASCADE,related_name="product_video_landing",null=True,blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_category.category_name

class ProductImageLand(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.FileField(upload_to=upload_product_image_landing_page)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class ProductLandingImage(models.Model):
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name="category_image_landing")
    image_category_land = models.ForeignKey(ProductImageLand,on_delete=models.CASCADE,related_name="product_image_landing",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_category.category_name
    
class TestimonialDetail(models.Model):
    image = models.ImageField(upload_to=upload_testimonial_landing_page)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name
class ProductTestimonials(models.Model):
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name="category_testimonial_landing")
    testimonial=models.ForeignKey(TestimonialDetail,on_delete=models.CASCADE,related_name="testimonial_category",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_category.category_name

