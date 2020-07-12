import json

from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from apps.auth_user.models import User


class AuthAPITest(APITestCase):
    url_base = "/login/"

    def setUp(self):
        self.superuser = mommy.make(User, email="w@gmail.com", is_superuser=True)
        self.superuser.set_password("123")
        self.superuser.save()

    def _decode_response(self, response):
        return json.loads(response.content.decode('utf8'))

    def test_login(self):
        data = {
            "email": "w@gmail.com",
            "password": "123"
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self._decode_response(response)
        self.assertNotEqual(response['token'], None)

    def test_create_user(self):
        data = {
            "email": "chaves@gmail.com",
            "full_name": "Chaves",
            "nick_name": "chapolim",
            "cpf": "116.323.234-35",
            "phone": "84 9991952-70",
            "sex": "M",
            "password": "123"
        }
        response = self.client.post("/auth_user/cadastrar/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_repeat_email(self):
        data = {
            "email": "w@gmail.com",
            "full_name": "Chaves",
            "nick_name": "chapolim",
            "cpf": "116.323.234-35",
            "phone": "84 9991952-70",
            "sex": "M",
            "password": "123"
        }
        response = self.client.post("/auth_user/cadastrar/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self._decode_response(response)
        self.assertEqual(response['email'][0], 'usuário com este endereço de email já existe.')

