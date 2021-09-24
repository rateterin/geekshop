from django.contrib import admin
from products.models import Category, Product


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'description', 'discount', 'is_active')
    fields = (('id', 'name'), ('discount', 'is_active'), 'image', 'description')
    readonly_fields = ('id',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'discount', 'quantity', 'category', 'is_active')
    fields = (('id', 'name'), ('category', 'is_active'), 'image', 'description', ('price', 'quantity', 'discount'))
    readonly_fields = ('id',)
    ordering = ('name', '-price')
    search_fields = ('name',)


