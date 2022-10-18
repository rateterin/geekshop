from django.db import models
from django.http import Http404

from authapp.models import ShopUser
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    @property
    def baskets(self):
        return Basket.objects.select_related("user").filter(user=self.user)

    @property
    def total(self):
        return sum([basket.quantity for basket in self.baskets])

    @property
    def total_sum(self):
        return sum(basket.sum() for basket in self.baskets)

    @staticmethod
    def get_item(pk=0):
        try:
            basket = Basket.objects.get(id=pk)
        except Basket.DoesNotExist:
            raise Http404
        else:
            return basket
