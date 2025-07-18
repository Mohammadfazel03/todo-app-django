from django.test import TestCase
from rest_framework.test import APIClient
from django.core import mail
from account.models import User


class TestAuthApi(TestCase):

    def setUp(self):
        self.active_user = User.objects.create_user(
            email='active@test.com',
            password='jenfbfuyhebfnei',
            is_active=True
        )
        self.inactive_user = User.objects.create_user(
            email='inactive@test.com',
            password='jenfbfuyhebfnei',
            is_active=False
        )
        self.client = APIClient()

    def test_register_user_200(self):
        data = {
            'email': 'test@email.com',
            'password': 'fkivuhfiuriffm',
            'password2': 'fkivuhfiuriffm',
            'is_active': True,
            'is_superuser': True,
            'is_staff': True
        }
        response = self.client.post('/api/v1/auth/register/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('email' in response.json())
        user = User.objects.get(email=response.json()['email'])
        self.assertIsNotNone(user)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], data['email'])

    def test_register_user_not_equal_password(self):
        data = {
            'email': 'test@email.com',
            'password': 'fkivuhfiurifdfdffm',
            'password2': 'fkivuhfiuriffm'
        }
        response = self.client.post('/api/v1/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email=data['email']).exists())

    def test_register_user_weak_password(self):
        data = {
            'email': 'test@email.com',
            'password': '1234',
            'password2': '1234'
        }
        response = self.client.post('/api/v1/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email=data['email']).exists())

    def test_register_user_already_exists(self):
        data = {
            'email': 'inactive@test.com',
            'password': 'fkivuhfiuriffm',
            'password2': 'fkivuhfiuriffm'
        }
        response = self.client.post('/api/v1/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.filter(email=data['email']).count(), 1)

    def test_register_user_without_email(self):
        data = {
            'password': 'fkivuhfiuriffm',
            'password2': 'fkivuhfiuriffm'
        }
        response = self.client.post('/api/v1/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_login_jwt_active_user(self):
        data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        response = self.client.post('/api/v1/jwt/login/', data=data)
        json_res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in json_res)
        self.assertTrue('refresh' in json_res)

    def test_login_jwt_inactive_user(self):
        data = {
            "email": 'inactive@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        response = self.client.post('/api/v1/jwt/login/', data=data)
        self.assertEqual(response.status_code, 401)

    def test_login_jwt_wrong_user(self):
        data = {
            "email": 'active@test.com',
            "password": 'jenfbf',
        }
        response = self.client.post('/api/v1/jwt/login/', data=data)
        self.assertEqual(response.status_code, 401)
