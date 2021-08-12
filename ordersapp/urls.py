import ordersapp.views as ordersapp
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = "ordersapp"

urlpatterns = [
   path('', login_required(ordersapp.OrderList.as_view()), name='orders_list'),
   path('forming/complete/<pk>', login_required(ordersapp.order_forming_complete), name='order_forming_complete'),
   path('create/', login_required(ordersapp.OrderItemsCreate.as_view()), name='order_create'),
   path('read/<pk>', login_required(ordersapp.OrderRead.as_view()), name='order_read'),
   path('update/<pk>', login_required(ordersapp.OrderItemsUpdate.as_view()), name='order_update'),
   path('delete/<pk>', login_required(ordersapp.OrderDelete.as_view()), name='order_delete'),
   path('product/<int:pk>/price/', ordersapp.get_product_price, name='get_product_price'),
]
