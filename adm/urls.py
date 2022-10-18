from django.urls import path

from adm.views import (
    index,
    AdmUserReadView,
    AdmUserCreateView,
    AdmUserUpdateView,
    AdmUserDeleteView,
)


app_name = "adm"

urlpatterns = [
    path("", index, name="index"),
    path("users/", AdmUserReadView.as_view(), name="users_read"),
    path("users/create/", AdmUserCreateView.as_view(), name="users_create"),
    path("users/update/<int:pk>/", AdmUserUpdateView.as_view(), name="users_update"),
    path("users/delete/<int:pk>/", AdmUserDeleteView.as_view(), name="users_delete"),
]
