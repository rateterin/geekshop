from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser, ShopUserProfile
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from django.utils.timezone import now
from datetime import timedelta


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'db.json')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            'django2',
            'django2@geekshop.local',
            'geekbrains'
        )

        self.user = ShopUser.objects.create_user(
            'tarantino',
            'tarantino@geekshop.local',
            'geekbrains'
        )

        self.user_with__first_name = ShopUser.objects.create_user(
            'umaturman',
            'umaturman@geekshop.local',
            'geekbrains',
            first_name='Ума'
        )

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['head']['title'], ' - Главная')
        self.assertNotContains(response, 'Выйти', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Выйти', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.url, '/auth/login/?next=/auth/profile/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['baskets']), [])
        self.assertEqual(response.request['PATH_INFO'], '/auth/profile/')
        self.assertIn(('Профиль' and 'Корзина'), response.content.decode())

    def test_user_logout(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['head']['title'], ' - Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'],
                          password=new_user_data['password1'])

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'],
                            status_code=200)

    # def test_user_wrong_register(self):
    #     new_user_data = {
    #         'username': 'teen',
    #         'first_name': 'Мэри',
    #         'last_name': 'Поппинс',
    #         'password1': 'geekbrains',
    #         'password2': 'geekbrains',
    #         'email': 'merypoppins@geekshop.local',
    #         'age': '17'}
    #
    #     url = reverse('authapp:register')
    #     response = self.client.post(url, data=new_user_data, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'ShopUserRegisterForm', 'age',
    #                          'Вы слишком молоды!')

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'authapp', 'ordersapp', 'baskets')


class TestModelsMethods(TestCase):
    def setUp(self) -> None:
        self.user_activation_key_expired = ShopUser.objects.create(
            username='user_1',
            email='mail1@example.com',
            password='simplepass',
            first_name='user_1_fname',
            last_name='user_1_lname',
            age=18,
            activation_key_expires=now() - timedelta(hours=1)
        )
        self.user_activation_key_not_expired = ShopUser.objects.create(
            username='user_2',
            email='mail2@example.com',
            password='simplepass',
            first_name='user_2_fname',
            last_name='user_2_lname',
            age=18,
            activation_key_expires=now() + timedelta(hours=1)
        )

    def test_user_is_activation_key_expired(self):
        self.assertTrue(self.user_activation_key_expired.is_activation_key_expired())
        self.assertFalse(self.user_activation_key_not_expired.is_activation_key_expired())

    def test_user_profile_created(self):
        self.assertTrue(
            ShopUserProfile.objects.select_related().filter(user=self.user_activation_key_expired).exists())
        self.assertTrue(
            ShopUserProfile.objects.select_related().filter(user=self.user_activation_key_not_expired).exists())

    def tearDown(self) -> None:
        pass
