from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'products/index.html')


def products(request):
    return render(request, 'products/products.html')
