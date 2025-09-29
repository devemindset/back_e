from django.contrib import admin
from .models import Order,OrderItem

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ("email","total_amount","full_name","address","phonenumber","status")

@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ("order","product_category","quantity","price",)

