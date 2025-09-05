from django.db import models
from django.utils.text import slugify
import os 

def upload_cover(instance,filename):
    base, ext = os.path.splitext(filename)
    clean_name = slugify(base)
    return f"commerce/cover/{instance.name}_{clean_name}{ext.lower()}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=upload_cover, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



