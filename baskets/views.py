from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F

from products.models import Product
from baskets.models import Basket


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    if not Basket.objects.select_related().filter(user=request.user, product=product).exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        Basket.objects.select_related().filter(user=request.user, product=product).update(quantity=F('quantity') + 1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id):
    Basket.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        if quantity >= 1:
            Basket.objects.filter(id=id).update(quantity=quantity)
        baskets = Basket.objects.select_related('user').filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/baskets.html', context)
        return JsonResponse({'result': result})
