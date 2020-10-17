from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.card.models import CardBingo
from apps.core.models import Bingo, Room
from apps.core.serializers import BingoSerializer, RoomSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

class BingoViewSet(viewsets.ModelViewSet):
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(methods=['GET'], detail=False)
    def buscar_bingo_ativo(self, request):
        bingo = Bingo.objects.filter(is_activated=True).first()
        serializer = BingoSerializer(instance=bingo).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def cadastrar_bingo(self, request):
        serializer = BingoSerializer(data={
            'name': 'Sala'
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def remover_user(self, room, user):
        room.users.remove(user)
        RoomSerializer(instance=room).data

    def atualizar_rooms(self, room):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'globals',
            {
                'type': "atualizar.room",
                'room':  RoomSerializer(instance=room).data
            }
        )

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        card = CardBingo.objects.filter(user=request.user, is_activate=True).first()
        room = Room.objects.filter(id=pk).first()
        print('Tem cartela:?', card)

        if not room:
            return Response({'error': {'message': "A sala não existe."}},
                            status=status.HTTP_400_BAD_REQUEST)

        if not card and room.game_iniciado == False:
            return Response({'error': {'message': "Escolha um cartelão para entrar na sala."}},
                            status=status.HTTP_400_BAD_REQUEST)

        if not card and room.game_iniciado == True and request.user not in room.users.all():
            return Response({'error': {'message': "Infelizmente, você não chegou a tempo. Aguarde a próxima rodada!"}},
                            status=status.HTTP_400_BAD_REQUEST)

        if room.is_pode_entrar(card=card):
            before_users = room.users.all()
            atualizar = request.user not in before_users
            print(atualizar)
            room.users.add(request.user)
            RoomSerializer(instance=room).data

            if atualizar:
                self.atualizar_rooms(room)
            return Response("Acesso permitido", status=status.HTTP_201_CREATED)
        else:
            # self.remover_user(room=room, user=request.user)
            return Response({'error': {'message': "Você não tem permissão para entrar nessa sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)
