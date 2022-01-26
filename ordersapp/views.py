from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from products.context_processors import set_head as head
from products.models import Product
from baskets.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if sender.objects.filter(pk=instance.pk).exists():
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        head.update(title=' - Список заказов', custom_css='')
        return Order.objects.filter(user=self.request.user).select_related()

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    template_name = 'ordersapp/order_form.html'
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            Basket.objects.select_related('user', 'product').filter(user=self.request.user).delete()
            formset = order_form_set(self.request.POST)
        else:
            basket_items = Basket.objects.select_related('user', 'product').filter(user=self.request.user)
            if len(basket_items):
                order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = order_form_set()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    delta_price = basket_items[num].product.price / 100 * basket_items[num].product.discount
                    price = basket_items[num].product.price - delta_price
                    form.initial['price'] = price
            else:
                formset = order_form_set()

        data['orderitems'] = formset
        head.update(title=' - Создание заказа', custom_css='')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    template_name = 'ordersapp/order_form.html'
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)

        if self.request.POST:
            data['orderitems'] = order_form_set(self.request.POST, instance=self.object)
        else:
            formset = order_form_set(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    price = form.instance.product.price
                    discount = form.instance.product.discount
                    form.initial['price'] = price
                    form.initial['discount'] = discount
                    form.initial['subtotal'] = form.instance.product.quantity * (price - price * discount / 100)
            data['orderitems'] = formset
        head.update(title=' - Редактирование заказа', custom_css='')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        head.update(title=' - Просмотр заказа', custom_css='')
        return context

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            discount = product.discount
            if not discount:
                discount = product.category.discount
            price = product.price - product.price / 100 * discount
            return JsonResponse({'price': price})
        else:
            return JsonResponse({'price': 0})
