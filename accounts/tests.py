from django.test import TestCase, Client
from django.urls import reverse_lazy

from .models import User
from .serializers import UserCreateSerializer


class UserCreateSerializerTest(TestCase):
    def test_user_create_success(self):
        data = {
            "username": "ali",
            "email": "giyos@gmail.com",
            "first_name": "salom",
            "last_name": "alik",
            'password': "12",
            're_password': "12"
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'ali')
        self.assertTrue(user.check_password('12'))

    def test_user_invalid_data(self):
        invalid_data = {
            "username": "ali",
            "email": "ali12@sasa.com",
            "first_name": "",
            "last_name": "alik",
            'password': "12",
            're_password': "1223"
        }
        serializer = UserCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_data = {
            "username": "ali",
            "email": "giyos@gmail.com",
            "first_name": "salom",
            "last_name": "alik",
            'password': "12",
            're_password': "12"
        }

        self.register_url = reverse_lazy('auth-list')
        self.login_url = reverse_lazy("jwt_login")

    def test_register_account(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_account_login(self):
        self.register_data.pop('re_password')
        User.objects.create_user(**self.register_data)
        response = self.client.post(self.login_url, {"username": "ali", "password": '12'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('access',response.json())
        self.assertIn('refresh',response.json())
