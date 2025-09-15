from django.db import models
from django.conf import settings
from products.models import ProductCategory
import uuid

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True, null=True,unique=True)  # Pour visiteurs non connectés
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.session_id:

            self.session_id = uuid.uuid4().hex[:6].upper()

            while Cart.objects.filter(session_id=self.session_id).exists():
                self.session_id = uuid.uuid4().hex[:6].upper()



        super().save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,related_name="product_category", null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_category.category_name} x {self.quantity}"
    
    
