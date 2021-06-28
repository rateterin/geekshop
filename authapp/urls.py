from django.urls import path
import authapp.views as authapp
from django.contrib.auth.decorators import login_required

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('profile/', login_required(authapp.profile), name='profile'),
]
