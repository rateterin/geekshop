from django.urls import path

import products.views as products


app_name = "products"

urlpatterns = [
    path("", products.products, name="index"),
    path("<int:pk>/", products.product, name="product"),
    path("category/<int:pk>/", products.products, name="category"),
    path("category/<int:pk>/page/<int:page>/", products.products, name="page"),
]
