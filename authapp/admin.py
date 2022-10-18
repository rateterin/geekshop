from django.contrib import admin
from authapp.models import ShopUser, ShopUserProfile
from baskets.admin import AdminBaskets


class AdminShopUserProfileInline(admin.TabularInline):
    model = ShopUserProfile
    fields = ()
    verbose_name = "Профиль"
    extra = 0


@admin.register(ShopUserProfile)
class AdminShopUserProfile(admin.ModelAdmin):
    pass


@admin.register(ShopUser)
class AdminUser(admin.ModelAdmin):
    inlines = (
        AdminShopUserProfileInline,
        AdminBaskets,
    )
