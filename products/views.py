from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, FormView
from django.http import Http404
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F, Q

import json
from products.models import Category, Product
from products.context_processors import set_head as head
from authapp.models import ShopUser


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Product)
def processing_discount_with_product_or_category_save(sender, instance, **kwargs):
    if instance.pk:
        if sender == Category:
            if sender.objects.filter(pk=instance.pk).exists():
                old_discount = 100 - sender.objects.values_list('discount').filter(pk=instance.pk)[0][0]
            else:
                old_discount = 100
            new_discount = 100 - instance.discount
            discount = new_discount / old_discount
            instance.product_set.filter(discount=0).update(price=F('price') * discount)
        if sender == Product:
            if sender.objects.filter(pk=instance.pk).exists():
                old_product_discount = 100 - sender.objects.values_list('discount').filter(pk=instance.pk)[0][0]
            else:
                old_product_discount = 100
            old_category_discount = 100
            old_category_discount -= Category.objects.values_list('discount').filter(pk=instance.category.pk)[0][0]
            new_product_discount = 100 - instance.discount
            if not (100 - old_product_discount):
                discount = new_product_discount / old_category_discount
            elif not (100 - new_product_discount):
                discount = old_category_discount / old_product_discount
            else:
                discount = new_product_discount / old_product_discount
            instance.price = float(instance.price) * discount


def home(request):
    head.update(title=' - Главная', custom_css='css/index.css')
    return render(request, 'products/index.html')


def product(request, pk=0):
    if not pk:
        raise Http404
    head.update(title=' - Продукт', custom_css='')
    context = {
        'product': Product.objects.get(pk=pk)
    }
    return render(request, 'products/product.html', context=context)


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
