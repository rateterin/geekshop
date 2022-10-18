from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class AdminOrders(admin.ModelAdmin):
    list_display = ("id", "user", "created", "updated", "status")
