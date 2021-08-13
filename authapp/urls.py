from django.urls import path, re_path
import authapp.views as authapp
from django.contrib.auth.decorators import login_required

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='activation_verify'),
    path('profile/', login_required(authapp.profile), name='profile'),
]
