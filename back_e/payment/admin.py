from django.contrib import admin
from .models import StripeProduct,Payment

@admin.register(StripeProduct)
class StipeProductAdmin(admin.ModelAdmin):
    list_display = ("name","stripe_product_id","amount",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user","email","amount","currency","created_at",)