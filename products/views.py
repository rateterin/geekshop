from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, FormView
from django.conf import settings
from django.core.cache import cache

import json
from products.models import Category, Product
from products.context_processors import set_head as head
from authapp.models import ShopUser


def home(request):
    head['custom_css'] = 'css/index.css'
    return render(request, 'products/index.html')


def products(request, pk=0, page=1):
    if not pk:
        goods = get_products()
        category = None
    else:
        goods = get_products_from_category(pk)
        category = get_category(pk)
    categories = get_all_categories()

    paginator = Paginator(goods, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    head.update(title=' - Каталог', custom_css='')
    context = {
        'products': products_paginator,
        'categories': categories,
        'selected_category': pk
    }
    if category:
        context.update(products_count=category.active_products_in_category)
    return render(request, 'products/products.html', context=context)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = Category.objects.select_related().filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return Category.objects.select_related().filter(is_active=True)


def get_all_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        _categories = cache.get(key)
        if _categories is None:
            _categories = Category.objects.all()
            cache.set(key, _categories)
        return _categories
    else:
        return Category.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        _category = cache.get(key)
        if _category is None:
            _category = get_object_or_404(Category, pk=pk)
            cache.set(key, _category)
        return _category
    else:
        return get_object_or_404(Category, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True).order_by('name').select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True).select_related('category')


def get_products_from_category(pk):
    if settings.LOW_CACHE:
        key = f'products_from_category_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category=pk).order_by('name').select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category=pk).order_by('name').select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        _product = cache.get(key)
        if _product is None:
            _product = get_object_or_404(Product, pk=pk)
            cache.set(key, _product)
        return _product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.select_related().filter(is_active=True).order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.select_related().filter(is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.select_related().filter(category__pk=pk, is_active=True).order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.select_related().filter(category__pk=pk, is_active=True).order_by('price')
