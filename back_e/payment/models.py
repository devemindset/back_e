from django.db import models
from custom_user.models import CustomUser

class StripeProduct(models.Model):

    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default='usd')
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.product_type})"


class Payment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    email = models.CharField(max_length=50,null=True,blank=True)
    stripe_payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.stripe_payment_id}"