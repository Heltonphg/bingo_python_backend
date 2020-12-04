from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.card.models import CardBingo
from apps.core.models import Bingo, Room
from apps.core.serializers import BingoSerializer, RoomSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.core.thred_iniciar import ThredVerifica
from apps.core.tread import ThredRegressive


class BingoViewSet(viewsets.ModelViewSet):
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(methods=['GET'], detail=False)
    def buscar_bingo_prox(self, request):
        bingo = Bingo.objects.filter(is_prox_stack=True).first()
        serializer = BingoSerializer(instance=bingo).data
        return Response(serializer, status=status.HTTP_200_OK)

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

    @receiver(post_save, sender=Bingo)
    def pos_save(sender, instance, created, **kwargs):
        if created:
            thredRegressive = ThredRegressive()
            thredRegressive.start()
            # verifica = ThredVerifica()
            # verifica.start()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'globals',
                {
                    'type': "reload.bingo",
                    'bingo': BingoSerializer(instance=instance).data
                }
            )


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
                'room': RoomSerializer(instance=room).data
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
            return Response(
                {'error': {'message': "Infelizmente, você não chegou a tempo. Deseja entrar na próxima sala?"}},
                status=status.HTTP_400_BAD_REQUEST)

        if room.is_pode_entrar(card=card):
            before_users = room.users.all()
            atualizar = request.user not in before_users
            room.users.add(request.user)
            RoomSerializer(instance=room).data

            if atualizar:
                self.atualizar_rooms(room)
            return Response("Acesso permitido", status=status.HTTP_201_CREATED)
        else:
            return Response({'error': {'message': "Acesso negado, pois você já está em uma sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=True)
    def entrar_prox_room(self, request, pk):
        card = CardBingo.objects.filter(user=request.user, is_activate=True).first()
        room = Room.objects.filter(id=pk).first()
        print('Tem cartela pra proxima partida:?', card)

        if not card:
            return Response({'error': {'message': "Escolha um cartelão para entrar na sala."}},
                            status=status.HTTP_400_BAD_REQUEST)
        if room.is_pode_entrar(card=card):
            room.users.add(request.user)
            RoomSerializer(instance=room).data
            self.atualizar_rooms(room)
            return Response("Acesso permitido", status=status.HTTP_201_CREATED)
        else:
            return Response({'error': {'message': "Acesso negado, pois você já está em uma sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False)
    def criar_prox_bingo(self, request):
        with transaction.atomic():
            prox_bingo = Bingo.objects.filter(is_prox_stack=True, is_activated=False).first()
            if prox_bingo:
                return Response(BingoSerializer(instance=prox_bingo).data, status=status.HTTP_200_OK)
            else:
                serializer = BingoSerializer(data={
                    'name': 'Sala'
                })
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
