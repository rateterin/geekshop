from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False)
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

    def __str__(self):
        return f'{self.name} | {self.category.name}'
