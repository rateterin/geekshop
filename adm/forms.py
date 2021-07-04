from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser


class AdmUserCreationForm(ShopUserRegisterForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'avatar')
