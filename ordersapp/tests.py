from django.test import TestCase
from baskets.models import Basket
from authapp.models import ShopUser
from ordersapp.models import Order, OrderItem
from django.http import Http404
from products.models import Category, Product
from django.utils.timezone import now
from datetime import timedelta


class TestOrdersAppModelsMethods(TestCase):
    def setUp(self) -> None:
        self.user = ShopUser.objects.create_user(
            "tarantino", "tarantino@geekshop.local", "geekbrains"
        )
        self.category = Category.objects.create(name="Category_1")
        self.product_1 = Product.objects.create(
            category=self.category, name="Product_1", price=1000, quantity=10
        )
        self.product_2 = Product.objects.create(
            category=self.category, name="Product_2", price=2000, quantity=20
        )
        self.order_1 = Order.objects.create(user=self.user)
        self.order_1.orderitems.create(
            order=self.order_1, product=self.product_1, quantity=2
        )
        self.order_1.orderitems.create(
            order=self.order_1, product=self.product_2, quantity=7
        )
        self.order_2 = Order.objects.create(user=self.user)
        self.order_item_1 = self.order_2.orderitems.create(
            order=self.order_2, product=self.product_1, quantity=20
        )
        self.order_item_2 = self.order_2.orderitems.create(
            order=self.order_2, product=self.product_2, quantity=70
        )

    def test_order_print(self):
        self.assertEqual(str(self.order_1), f"Текущий заказ: {self.order_1.id}")

    def test_order_get_total_quantity(self):
        self.assertEqual(self.order_1.get_total_quantity(), 9)

    def test_order_get_product_type_quantity(self):
        self.assertEqual(len(self.order_1.orderitems.all()), 2)

    def test_order_get_total_cost(self):
        self.assertEqual(self.order_1.get_total_cost(), 16000)

    def test_order_get_summary(self):
        self.assertEqual(
            self.order_1.get_summary(), {"total_cost": 16000, "total_quantity": 9}
        )

    def test_order_delete(self):
        order_id = self.order_1.id
        items = self.order_1.orderitems
        products_quantities, order_items_quantities = [], []
        for n, item in enumerate(items):
            products_quantities[n] = item.product.quantity
            order_items_quantities[n] = item.quantity
        self.order_1.delete()
        self.assertFalse(Order.objects.filter(id=order_id).exists())
        for n, item in enumerate(items):
            self.assertTrue(
                Product.objects.filter(pk=item.product.pk).values_list("quantity")[0],
                products_quantities[n] + order_items_quantities[n],
            )

    def test_order_item_get_product_cost(self):
        self.assertEqual(self.order_item_1.get_product_cost(), 1000)
        self.assertEqual(
            self.order_item_2.get_item(self.order_item_1.pk), self.order_item_1
        )
        self.assertRaises(Http404, self.order_item_2.get_item(0))

    def tearDown(self) -> None:
        pass
