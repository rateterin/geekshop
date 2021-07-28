"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from django.conf.urls.static import static
from django.conf.urls import include
import products.views as products

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', products.home, name='home'),
    path('products/', include('products.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('baskets/', include('baskets.urls', namespace='baskets')),
    path('adm/', include('adm.urls', namespace='adm')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
    path('', include('social_django.urls', namespace='social')),
]

if not settings.DEBUG:
    if settings.MEDIA_ROOT and settings.STATIC_ROOT:
        urlpatterns += url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        urlpatterns += url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
