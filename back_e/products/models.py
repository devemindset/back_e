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

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
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
    currencyCode = models.CharField(max_length=3,null=True,blank=True)
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



