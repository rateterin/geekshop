from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from authapp.models import ShopUser
from products.context_processors import set_head as head
from adm.forms import AdmUserCreationForm, AdmUserUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def index(request):
    return render(request, "adm/admin.html")


class AdmUserReadView(ListView):
    model = ShopUser
    template_name = "adm/admin-users-read.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        head["title"] = " - Админка | список пользователей"
        # context.update({'head': {'descr': '', 'author': '', 'title': ' - Админка | список пользователей'}})
        return context


class AdmUserCreateView(CreateView):
    model = ShopUser
    template_name = "adm/admin-users-create.html"
    form_class = AdmUserCreationForm
    success_url = reverse_lazy("adm:users_read")

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        head["title"] = " - Админка | создание пользователя"
        # context.update({'head': {'descr': '', 'author': '', 'title': ' - Админка | создание пользователя'}})
        return context


class AdmUserUpdateView(UpdateView):
    model = ShopUser
    template_name = "adm/admin-users-update-delete.html"
    form_class = AdmUserUpdateForm
    success_url = reverse_lazy("adm:users_read")

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        head.update(title=" - Профиль", custom_css="css/profile.css")
        # context.update({'head': {'descr': '', 'author': '', 'title': ' - Профиль', 'custom_css': 'css/profile.css'}})
        return context


class AdmUserDeleteView(DeleteView):
    model = ShopUser
    template_name = "adm/admin-users-update-delete.html"
    success_url = reverse_lazy("adm:users_read")

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def delete(self, request, *args, **kwargs):
        super().delete(self, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())
