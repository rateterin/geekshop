import subprocess
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from django.conf import settings
from django.core.mail import EmailMessage
from authapp.forms import (
    ShopUserLoginForm,
    ShopUserRegisterForm,
    ShopUserProfileForm,
    ShopUserProfileExtraForm,
)
from authapp.models import ShopUser
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from baskets.models import Basket
from products.context_processors import set_head as head
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView
from django.db import transaction


def send_activation_code(user):
    verify_link = reverse(
        "authapp:activation_verify", args=(user.email, user.activation_key)
    )
    title = f"Активация учетной записи на сайте {settings.DOMAIN_NAME}"
    message = (
        f"Для активации учетной записи {user.username} на сайте {settings.DOMAIN_NAME} перейдите по ссылке: "
        f"\n{settings.DOMAIN_NAME}{verify_link}"
    )
    # Note: send_mail
    # The API for this method is frozen.
    # New code wanting to extend the functionality should use the EmailMessage class directly.

    # return send_mail(subject=title,
    #                  message=message,
    #                  from_email=settings.EMAIL_HOST_USER,
    #                  recipient_list=(user.email,),
    #                  fail_silently=False)
    res = EmailMessage(
        subject=title,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=(user.email,),
    ).send(False)
    return res


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email, activation_key=activation_key)
    if user.exists():
        if user[0].activation_key_expires >= now() and not user[0].is_active:
            messages.success(request, "Ваша учетная запись успешно активирована.")
            user.update(is_active=True)

            head.update(title=" - Вход", custom_css="css/auth-admin.css")
            context = {
                "div_wrap_class": "col-lg-5",
                "h3_title": "Авторизация",
                "form": ShopUserLoginForm,
                "form_link": "authapp:register",
                "form_link_text": "Нужен аккаунт? Зарегистрируйся!",
            }
            return render(request, "authapp/login.html", context=context)
        else:
            messages.warning(request, "Учетная запись не активирована!")
    else:
        messages.warning(request, "Учетная запись не активирована!")
    return HttpResponseRedirect(reverse("authapp:login"))


def login(request):
    if request.method == "POST":
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                return HttpResponseRedirect(reverse("home"))
    else:
        login_form = ShopUserLoginForm()
    head.update(title=" - Вход", custom_css="css/auth-admin.css")
    context = {
        "div_wrap_class": "col-lg-5",
        "h3_title": "Авторизация",
        "form": login_form,
        "form_link": "authapp:register",
        "form_link_text": "Нужен аккаунт? Зарегистрируйся!",
    }
    return render(request, "authapp/login.html", context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("home"))


# class UserRegisterView(CreateView):
#     form_class = ShopUserRegisterForm
#     template_name = 'authapp/register.html'
#     success_url = reverse_lazy('authapp:login')


def register(request):
    if request.method == "POST":
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_activation_code(user=user):
                messages.success(request, f"Вы успешно зарегистрировались!")
                messages.success(
                    request, f"На указанную почту отправлена ссылка для активации."
                )
                return HttpResponseRedirect(reverse("authapp:register"))
            else:
                messages.warning(request, "Ошибка отправки ссылки для активации!")
    else:
        register_form = ShopUserRegisterForm()
    head.update(title=" - Регистрация", custom_css="css/auth-admin.css")
    context = {
        "div_wrap_class": "col-lg-7",
        "form": register_form,
        "h3_title": "Создать аккаунт",
        "form_link": "authapp:login",
        "form_link_text": "Уже есть аккаунт? Авторизоваться",
    }
    return render(request, "authapp/register.html", context=context)


@login_required
@transaction.atomic
def profile(request):
    if request.method == "POST":
        user_form = ShopUserProfileForm(
            data=request.POST, files=request.FILES, instance=request.user
        )
        profile_form = ShopUserProfileExtraForm(
            request.POST, request.FILES, instance=request.user.shopuserprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("authapp:profile"))
    else:
        user_form = ShopUserProfileForm(instance=request.user)
        profile_form = ShopUserProfileExtraForm(instance=request.user.shopuserprofile)

    baskets = Basket.objects.select_related("user", "product").filter(user=request.user)
    head.update(title=" - Профиль", custom_css="css/profile.css")
    context = {
        "div_wrap_class": "col-lg-7",
        "form": user_form,
        "form2": profile_form,
        "baskets": baskets,
    }
    return render(request, "authapp/profile.html", context=context)
