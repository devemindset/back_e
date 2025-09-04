from django.db import models

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
