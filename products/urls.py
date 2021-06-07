from django.urls import path

import products.views as products


app_name = 'products'

urlpatterns = [
    path('', products.products, name='index'),
    path('<int:cid>/', products.products, name='category'),
]
