from django.contrib import admin
from products.models import Category, Product

# Register your models here.
admin.site.register(Category)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'category', 'is_active')
    fields = (('id', 'name'), ('category', 'is_active'), 'image', 'description', ('price', 'quantity'))
    readonly_fields = ('id',)
    ordering = ('name', '-price')
    search_fields = ('name',)


