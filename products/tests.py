from django.test import TestCase
from django.test.client import Client
from .models import Product, Category
from django.core.management import call_command


class TestProductsSmoke(TestCase):
    def setUp(self):
        call_command("flush", "--noinput")
        call_command("loaddata", "db.json")
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

        for category in Category.objects.all():
            response = self.client.get(f"/products/category/{category.pk}/")
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f"/products/{product.pk}/")
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command("sqlsequencereset", "products", "authapp", "ordersapp", "baskets")


class TestProductsProductModelMethods(TestCase):
    def setUp(self) -> None:
        self.category_1 = Category.objects.create(name="Обувь")
        self.product_1 = Product.objects.create(
            category=self.category_1, name="Product_1", quantity=1, price=1000
        )
        self.product_2 = Product.objects.create(
            category=self.category_1, name="Product_2", quantity=1, price=1000
        )
        self.product_3 = Product.objects.create(
            category=self.category_1,
            name="Product_3",
            quantity=1,
            price=1000,
            is_active=False,
        )

    def test_product_get(self):
        product_1 = Product.objects.get(name="Product_1")
        product_2 = Product.objects.get(name="Product_2")
        product_3 = Product.objects.get(name="Product_3")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)
        self.assertEqual(product_3, self.product_3)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Product_1")
        product_2 = Product.objects.get(name="Product_2")
        product_3 = Product.objects.get(name="Product_3")
        self.assertEqual(str(product_1), "Product_1")
        self.assertEqual(str(product_2), "Product_2")
        self.assertEqual(str(product_3), "Product_3")

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Product_1")
        product_2 = Product.objects.get(name="Product_2")
        product_3 = Product.objects.get(name="Product_3")
        active_products = product_2.get_items()
        self.assertIn((product_1 and product_2), list(active_products))

    def tearDown(self) -> None:
        pass
