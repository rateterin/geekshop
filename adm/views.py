from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from authapp.models import ShopUser
from adm.forms import AdmUserCreationForm


def index(request):
    return render(request, 'adm/admin.html')


def adm_users(request):
    context = {'users': ShopUser.objects.all()}
    return render(request, 'adm/admin-users-read.html', context=context)


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


def adm_users_update(request, id):
    return render(request, 'adm/admin-users-update-delete.html')


def adm_users_delete(request, id):
    pass
