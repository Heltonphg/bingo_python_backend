from rest_framework import viewsets, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.auth_user.models import User
from apps.card.models import CardBingo
from apps.core.models import Bingo, Room
from apps.core.serializers import BingoSerializer, RoomSerializer

from datetime import datetime


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

        serializer = BingoSerializer(data={
            'name': name_bingo,
            'time_initiation': hoje
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        try:
            card = CardBingo.objects.get(user_id=request.user, is_activate=True)
        except CardBingo.DoesNotExist:
            raise serializers.ValidationError('O card nao existe')

        room = Room.objects.filter(id=pk).first()
        if not room:
            raise serializers.ValidationError('A sala nao existe')

        if room.is_pode_entrar(card=card):
            serializer = RoomSerializer(instance=room).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': {'message': "Ops, Você não tem permissão para entrar nessa sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)
