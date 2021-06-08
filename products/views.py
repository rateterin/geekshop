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
    if not cid:
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category=cid)
    categories = Category.objects.all()

    return render(request, 'products/products.html', context={
        'head': {'descr': '', 'author': '', 'title': ' - Каталог', 'custom_css': 'css/products.css'},
        'products': goods,
        'categories': categories,
        'selected_category': cid or 0
    })
