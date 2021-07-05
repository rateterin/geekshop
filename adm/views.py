from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from authapp.models import ShopUser
from adm.forms import AdmUserCreationForm, AdmUserUpdateForm
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def index(request):
    return render(request, 'adm/admin.html')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def adm_users(request):
    context = {'users': ShopUser.objects.all()}
    return render(request, 'adm/admin-users-read.html', context=context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def adm_users_create(request):
    if request.method == 'POST':
        form = AdmUserCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан!')
            return HttpResponseRedirect(reverse('adm:users_read'))
    else:
        form = AdmUserCreationForm()

    context = {
        'head': {'descr': '',
                 'author': '',
                 'title': ' - Админка | создание пользователя'},
        'form': form,
        'h3_title': 'Создание пользователя'}
    return render(request, 'adm/admin-users-create.html', context=context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def adm_users_update(request, id):
    user_for_update = ShopUser.objects.get(id=id)
    if request.method == 'POST':
        form = AdmUserUpdateForm(data=request.POST, files=request.FILES, instance=user_for_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adm:users_read'))
    else:
        form = AdmUserUpdateForm(instance=user_for_update)
        context = {
            'head': {'descr': '', 'author': '', 'title': ' - Профиль', 'custom_css': 'css/profile.css'},
            'div_wrap_class': 'col-lg-7',
            'form': form,
            'user_for_update': user_for_update,
        }
        return render(request, 'adm/admin-users-update-delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def adm_users_delete(request, id):
    user = ShopUser.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('adm:users_read'))
