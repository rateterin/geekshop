from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.models import Category, Product
from authapp.models import ShopUser
from django.views.generic import View, ListView, FormView

import json


# Create your views here.


def home(request):
    return render(request, 'products/index.html', context={
        'head': {'descr': '', 'author': '', 'title': '', 'custom_css': 'css/index.css'}
    })


def products(request, pk=None, page=1):
    if not pk:
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category=pk)
    categories = Category.objects.all()

    paginator = Paginator(goods, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    return render(request, 'products/products.html', context={
        'head': {'descr': '', 'author': '', 'title': ' - Каталог', 'custom_css': 'css/products.css'},
        'products': products_paginator,
        'categories': categories,
        'selected_category': pk or 0
    })
