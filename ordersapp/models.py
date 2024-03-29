from django.db import models
from django.db.models import F
from django.http import Http404

from django.conf import settings
from products.models import Product


class Order(models.Model):
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PROCEEDED = "PRD"
    PAID = "PD"
    READY = "RDY"
    CANCEL = "CNC"

    ORDER_STATUS_CHOICES = (
        (FORMING, "формируется"),
        (SENT_TO_PROCEED, "отправлен в обработку"),
        (PAID, "оплачен"),
        (PROCEEDED, "обрабатывается"),
        (READY, "готов к выдаче"),
        (CANCEL, "отменен"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлен", auto_now=True)
    status = models.CharField(
        verbose_name="статус",
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING,
    )
    is_active = models.BooleanField(verbose_name="активен", default=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Текущий заказ: {self.id}"

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum((item.quantity for item in items))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        # return sum(list(map(lambda x: x.quantity * x.product.price, items)))
        return sum((item.quantity * item.product.price for item in items))

    def delete(self):
        for item in self.orderitems.select_related():
            # item.product.update(quantity=F('quantity') + item.quantity)
            Product.objects.filter(pk=item.product.pk).update(
                quantity=F("quantity") + item.quantity
            )
            # item.product.save()

        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            # 'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            # 'total_quantity': sum(list(map(lambda x: x.quantity, items)))
            "total_cost": sum((item.quantity * item.product.price for item in items)),
            "total_quantity": sum((item.quantity for item in items)),
        }


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name="продукт", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk=0):
        if OrderItem.objects.filter(id=pk).exists():
            return OrderItem.objects.get(id=pk)
        raise Http404
