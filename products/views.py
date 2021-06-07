from django.shortcuts import render, redirect
from products.models import Category, Product


import json

# Create your views here.


def home(request):
    return render(request, 'products/index.html', context={
        'head': {'descr': '', 'author': '', 'title': '', 'custom_css': 'css/index.css'}
    })


def products(request, cid=None):
    print(cid)
    with open('products/fixtures/products.json', 'r') as f:
        products = Product.objects.all()

    return render(request, 'products/products.html', context={
        'head': {'descr': '', 'author': '', 'title': ' - Каталог', 'custom_css': 'css/products.css'},
        'products': products
    })
