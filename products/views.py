from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, FormView

import json
from products.models import Category, Product
from products.context_processors import set_head as head
from authapp.models import ShopUser


def home(request):
    head['custom_css'] = 'css/index.css'
    return render(request, 'products/index.html')


def products(request, pk=None, page=1):
    if not pk:
        goods = Product.objects.all().order_by('name')
    else:
        goods = Product.objects.filter(category=pk).order_by('name')
    categories = Category.objects.all()

    paginator = Paginator(goods, 6)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    head.update(title=' - Каталог', custom_css='')
    return render(request, 'products/products.html', context={
        'products': products_paginator,
        'categories': categories,
        'selected_category': pk or 0
    })
