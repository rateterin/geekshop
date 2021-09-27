from django.db import models
from django.utils.functional import cached_property
from django.db.models.aggregates import Count
from django.db.models import Q


class Category(models.Model):
    DISCOUNT_CHOICES = [(n, f'{n} %') for n in range(100)]

    name = models.CharField(max_length=20, unique=True, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='category_images', blank=True)
    is_active = models.BooleanField(default=False)
    discount = models.PositiveSmallIntegerField(choices=DISCOUNT_CHOICES, default=0)

    def __str__(self):
        return self.name

    @cached_property
    def active_products_in_category(self):
        res = list(
            Product.objects.select_related().filter(category=self.id).values('category').annotate(c=Count('category')))
        if res:
            return res[0]['c']


class Product(models.Model):
    DISCOUNT_CHOICES = [(n, f'{n} %') for n in range(100)]

    name = models.CharField(max_length=64, unique=False, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='products_images', blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Опубликован', default=False, db_index=True)
    discount = models.PositiveSmallIntegerField(choices=DISCOUNT_CHOICES, default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_items():
        return Product.objects.select_related().filter(is_active=True).order_by('category', 'name')
