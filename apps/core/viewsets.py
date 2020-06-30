from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Bingo, Room
from apps.core.serializers import BingoSerializer, RoomSerializer
from apps.users.models import User, CardBingo
from datetime import datetime


class BingoViewSet(viewsets.ModelViewSet):
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(methods=['post'], detail=False)
    def cadastrar_bingo(self, request):
        hoje = datetime.now()
        hora = hoje.hour
        name_bingo = 'Bindo '
        if hora >= 0 and hora < 6:
            name_bingo += 'da Madrugada'
        elif hora >= 6 and hora < 12:
            name_bingo += 'da Manhã'
        elif hora >= 12 and hora < 13:
            name_bingo += 'do Meio-Dia'
        elif hora >= 13 and hora < 18:
            name_bingo += 'da Tarde'
        elif hora >= 18 and hora < 24:
            name_bingo += 'da Noite'

        bingo = {
            'name': name_bingo,
            'time_initiation': hoje
        }

        serializer = BingoSerializer(data=bingo)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    self.create_two_room(serializer.data['id'])
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def criar_bingo(self, room):
        Room.objects.create(
            bingo_id=room['bingo_id'], minumum_quantity=room['minumum_quantity'], type=room['type'],
            value_card=room['value_card']
        )

    def create_two_room(self, bingo_id):
        for i in range(1, 3):
            if i == 1:
                vip = {
                    'bingo_id': bingo_id,
                    'type': "V",
                    'value_card': 2,
                    'minumum_quantity': 15,
                }
                self.criar_bingo(vip)
            else:
                gratis = {
                    'bingo_id': bingo_id,
                    'type': "G",
                    'value_card': 0,
                    'minumum_quantity': 10,
                }
                self.criar_bingo(gratis)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        user = User.objects.get(id=self.request.data.get('user'))
        card = CardBingo.objects.get(user_id=user.pk, is_activate=True)
        room = Room.objects.get(id=pk)
        if room.is_pode_entrar(card=card):
            room.users.add(user)
            serializer = RoomSerializer(instance=room).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': {'message': "Ops, Você não tem permissão para entrar nessa sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)
