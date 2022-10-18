from django.test import TestCase
from baskets.models import Basket
from authapp.models import ShopUser
from django.http import Http404
from products.models import Category, Product


class TestBasketModelMethods(TestCase):
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
        self.basket_1 = Basket.objects.create(
            user=self.user, product=self.product_1, quantity=5
        )
        self.basket_2 = Basket.objects.create(
            user=self.user, product=self.product_2, quantity=10
        )

    def test_basket_get_items(self):
        self.assertEqual(self.basket_1.get_item(self.basket_1.pk), self.basket_1)
        self.assertEqual(self.basket_2.get_item(self.basket_2.pk), self.basket_2)
        self.assertRaises(Http404, self.basket_1.get_item, 0)

    def test_basket_print(self):
        self.assertEqual(
            str(self.basket_1), f"Корзина для tarantino | Продукт Product_1"
        )
        self.assertEqual(
            str(self.basket_2), f"Корзина для tarantino | Продукт Product_2"
        )

    def test_basket_sum(self):
        self.assertEqual(self.basket_1.sum(), 5000)
        self.assertEqual(self.basket_2.sum(), 20000)

    def test_basket_baskets(self):
        self.assertIn((self.basket_1 and self.basket_2), self.basket_1.baskets)

    def test_basket_total(self):
        self.assertEqual(self.basket_1.total, 15)

    def test_basket_total_sum(self):
        self.assertEqual(self.basket_1.total_sum, 25000)

    def tearDown(self) -> None:
        pass
