from django.urls import path

from adm.views import index, adm_users, adm_users_create, adm_users_update, adm_users_delete


app_name = 'adm'

urlpatterns = [
    path('', index, name='index'),
    path('users/', adm_users, name='users_read'),
    path('users/create/', adm_users_create, name='users_create'),
    path('users/update/<int:id>/', adm_users_update, name='users_update'),
    path('users/delete/<int:id>/', adm_users_delete, name='users_delete'),
]
