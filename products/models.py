from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='category_images', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, unique=False, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='products_images', blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Опубликован', default=False, db_index=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
