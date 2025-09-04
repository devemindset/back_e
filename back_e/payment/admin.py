from django.contrib import admin
from .models import StripeProduct

@admin.register(StripeProduct)
class StipeProductAdmin(admin.ModelAdmin):
    list_display = ("name","stripe_product_id","amount",)