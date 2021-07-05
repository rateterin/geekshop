from django.contrib import admin
from authapp.models import ShopUser
from baskets.admin import AdminBaskets


@admin.register(ShopUser)
class AdminUser(admin.ModelAdmin):
    inlines = (AdminBaskets,)
