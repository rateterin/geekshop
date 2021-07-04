from django.shortcuts import render


def index(request):
    return render(request, 'adm/admin.html')


def adm_users(request):
    return render(request, 'adm/admin-users-read.html')


def adm_users_create(request):
    return render(request, 'adm/admin-users-create.html')


def adm_users_update(request, id):
    return render(request, 'adm/admin-users-update-delete.html')


def adm_users_delete(request, id):
    pass
