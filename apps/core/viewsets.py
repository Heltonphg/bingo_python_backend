from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Event, Room
from apps.core.serializers import EventSerializer, RoomSerializer
from apps.users.models import User, CardBingo
from datetime import datetime, date
from apps.users.serializers import CardBingoSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(methods=['post'], detail=False)
    def cadastrar_evento(self, request):
        hoje = datetime.now()
        hora = hoje.hour
        name_event = 'Bindo '
        if hora >= 0 and hora < 6:
            name_event += 'da Madrugada'
        elif hora >= 6 and hora < 12:
            name_event += 'da Manhã'
        elif hora >= 12 and hora < 13:
            name_event += 'do Meio-Dia'
        elif hora >= 13 and hora < 18:
            name_event += 'da Tarde'
        elif hora >= 18 and hora < 24:
            name_event += 'da Noite'

        data = {
            'name': name_event,
            'time_initiation': hoje
        }

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            self.create_two_room(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def criar_sala(self, room):
        price = room['value_card']
        Room.objects.create(
            event_id=room['event_id'], minumum_quantity=room['minumum_quantity'], type=room['type'], value_card=price
        )

    def create_two_room(self, event_id):
        for i in range(1, 3):
            if i == 1:
                vip = {
                    'event_id': event_id,
                    'type': "V",
                    'value_card': 2,
                    'minumum_quantity': 15,
                }
                self.criar_sala(vip)
            else:
                gratis = {
                    'event_id': event_id,
                    'type': "G",
                    'value_card': 0,
                    'minumum_quantity': 10,
                }
                self.criar_sala(gratis)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        user = User.objects.get(id=self.request.data.get('user'))
        card = CardBingo.objects.get(user_id=user.pk, is_activate=True)
        room = Room.objects.get(id=pk)
        if card.is_activate and room.pk == card.room_id:
            room.users.add(user)
            serializer = RoomSerializer(instance=room).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': {'message': "Ops, Você não tem permissão para entrar nessa sala!"}},
                            status=status.HTTP_401_UNAUTHORIZED)
