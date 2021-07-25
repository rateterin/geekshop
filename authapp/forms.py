import random
import hashlib
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms

from .models import ShopUser, ShopUserProfile


class BaseRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'}), required=True, )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите адрес эл. почты'}), required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control', 'placeholder': 'Загрузите аватар'}), required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'avatar')
        exclude = ('age',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(BaseRegisterForm):
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите Ваш возраст'}), required=True)

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if ShopUser.objects.filter(email=data):
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован!')
        return data

    def save(self):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode(encoding='utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode(encoding='utf8')).hexdigest()
        user.save()
        return user


class ShopUserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = ShopUser
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'avatar':
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


class ShopUserProfileExtraForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ShopUserProfile.GENDER_CHOICES,
                               widget=forms.Select(choices=ShopUserProfile.GENDER_CHOICES),
                               required=False)
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                               max_length=256,
                               required=False)
    tagline = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              max_length=64,
                              required=False)

    class Meta:
        model = ShopUserProfile
        fields = ('gender', 'about_me', 'tagline')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileExtraForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
