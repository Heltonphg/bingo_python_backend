from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import Room



class BingoAPITest(APITestCase):
    url_base = "/bingos"

    def criar(self):
        return self.client.post("{}/cadastrar_bingo/".format(self.url_base))

    def test_criar_sala(self):
        response = self.criar()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verificar_salas(self):
        self.criar()
        response = Room.objects.all()
        self.assertEqual(response.count(), 2)

    def test_nao_permitir_criar_dois_bingos(self):
        self.criar()
        response = self.criar()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


