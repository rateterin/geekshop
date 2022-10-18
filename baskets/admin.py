from django.contrib import admin

from baskets.models import Basket


class AdminBaskets(admin.TabularInline):
    model = Basket
    fields = ("product", "quantity", "created_timestamp")
    readonly_fields = ("created_timestamp",)
    verbose_name = "Корзины"
    extra = 0
