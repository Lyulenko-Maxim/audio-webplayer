from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class AuthenticationTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.register_data = {
            "username": "admin",
            "password": "admin",
            "email": "email@email.com",
            "date_of_birth": "2002-08-03"
        }
        self.login_data = {
            "username": "admin",
            "password": "admin",
        }
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_01_user_registration(self):
        response = self.client.post(
            path = self.register_url,
            data = self.register_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_02_user_login(self):
        user = User.objects.create_user(**self.register_data)
        user.save()

        response = self.client.post(
            path = self.login_url,
            data = self.login_data,
        )

        cookies = response.cookies
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(cookies)
        self.assertIn('access_token', cookies)
        self.assertIn('refresh_token', cookies)
        self.assertIn('httponly', cookies['access_token'])
        self.assertIn('httponly', cookies['refresh_token'])

    def test_03(self):
        print(self.client.request)
