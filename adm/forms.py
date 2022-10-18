from authapp.forms import BaseRegisterForm, ShopUserProfileForm
from django import forms


class AdmUserCreationForm(BaseRegisterForm):
    pass


class AdmUserUpdateForm(ShopUserProfileForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": False})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control", "readonly": False})
    )
