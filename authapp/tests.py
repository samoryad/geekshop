from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')

        self.user = ShopUser.objects.create_user('test1', 'test1@geekshop.local', 'geekbrains')

        self.user_with__first_name = ShopUser.objects.create_user('test2', 'test2@geekshop.local', 'geekbrains',
                                                                  first_name='test2')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        # self.assertEqual(response.context['title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='django', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        # главная после логина
        # response = self.client.get('/')
        # self.assertContains(response, 'Пользователь', status_code=200)
        # self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
