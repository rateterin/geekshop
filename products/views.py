from django.shortcuts import render, redirect

import json

# Create your views here.


def home(request):
    return render(request, 'products/index.html', context={
        'head': {'descr': '', 'author': '', 'title': '', 'custom_css': 'css/index.css'}
    })


def products(request):
    with open('products/fixtures/products.json', 'r') as f:
        products = json.load(f)

    return render(request, 'products/products.html', context={
        'head': {'descr': '', 'author': '', 'title': ' - Каталог', 'custom_css': 'css/products.css'},
        'products': products
    })
