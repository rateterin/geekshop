from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserProfileForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from baskets.models import Basket
from functools import reduce


def login(request):
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        login_form = ShopUserLoginForm()
    context = {
        'head': {'descr': '', 'author': '', 'title': ' - Вход', 'custom_css': 'css/auth-admin.css'},
        'div_wrap_class': 'col-lg-5',
        'h3_title': 'Авторизация',
        'form': login_form,
        'form_link': 'authapp:register',
        'form_link_text': 'Нужен аккаунт? Зарегистрируйся!'}
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'head': {'descr': '', 'author': '', 'title': ' - Регистрация', 'custom_css': 'css/auth-admin.css'},
        'div_wrap_class': 'col-lg-7',
        'form': register_form,
        'h3_title': 'Создать аккаунт',
        'form_link': 'authapp:login',
        'form_link_text': 'Уже есть аккаунт? Авторизоваться'}
    return render(request, 'authapp/register.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ShopUserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        profile_form = ShopUserProfileForm(instance=request.user)

    context = {
        'head': {'descr': '', 'author': '', 'title': ' - Профиль', 'custom_css': 'css/profile.css'},
        'div_wrap_class': 'col-lg-7',
        'form': profile_form,
        'baskets': Basket.objects.filter(user=request.user),
        'total': reduce(lambda a, b: a + b,
                        [basket.quantity for basket in Basket.objects.filter(user=request.user)],
                        0),
        'total_sum': reduce(lambda a, b: a + b,
                            [basket.product.price * basket.quantity
                             for basket in Basket.objects.filter(user=request.user)],
                            0)
    }
    return render(request, 'authapp/profile.html', context=context)
