from django.core.management.base import BaseCommand
from products.models import Product
from ordersapp.models import OrderItem
from django.db.models import Q, F, When, Case, DecimalField


class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Product.objects.filter(Q(category__name='Одежда') | Q(category__name='Новинки'))
        print(f'{"Product name":^50} | {"Category name"}')
        for e in q:
            print(f'{e.name:50} | {e.category.name}')

        print('\r\n' * 2)
        q10 = Q(quantity__gt=10)
        q50 = Q(quantity__gt=50)
        d10 = 1 - .1
        d50 = 1 - .2
        pd = Q(product__discount__gt=0)
        cd = Q(product__category__discount__gt=0)
        pd_price = F('product__price') * F('product__discount')
        cd_price = F('product__price') * F('product__category__discount')

        print(
            f'{"id заказа":^15} | {"id позиции":^15} | {"Наименование товара":^64} | {"Количество"} |'
            f' {"Стоимость":^20} | {"Стоимость со скидкой"}')

        order_items = OrderItem.objects.annotate(
            item_cost=Case(
                When(q10, then=Case(
                    When(pd, then=pd_price * d10),
                    When(cd, then=cd_price * d10),
                    default=F('product__price') * F('quantity') * d10,
                    output_field=DecimalField(max_digits=2))),
                When(q50, then=Case(
                    When(pd, then=pd_price * d50),
                    When(cd, then=cd_price * d50),
                    default=F('product__price') * F('quantity') * d50,
                    output_field=DecimalField(max_digits=2))))).select_related()

        for order_item in order_items:
            print(
                f'{order_item.order.pk:15} | {order_item.pk:15} | {order_item.product.name:64s} | '
                f'{order_item.quantity:10} | {order_item.get_product_cost():20} | {order_item.item_cost}')
