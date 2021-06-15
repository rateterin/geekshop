from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserRegisterForm
from django.contrib import auth, messages
from django.urls import reverse


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST':
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
        else:
            print(login_form.errors)

    context = {'title': 'вход',
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
    title = 'Регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(register_form.errors)
    else:
        register_form = ShopUserRegisterForm()

    context = {'title': 'Регистрация',
               'div_wrap_class': 'col-lg-7',
               'form': register_form,
               'h3_title': 'Создать аккаунт',
               'form_link': 'authapp:login',
               'form_link_text': 'Уже есть аккаунт? Авторизоваться'}
    return render(request, 'authapp/register.html', context=context)


def profile(request):
    return HttpResponseRedirect(reverse('home'))
