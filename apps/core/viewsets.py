from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Event, Room
from apps.core.serializers import EventSerializer, RoomSerializer
from apps.users.models import User, CardBingo
from apps.users.serializers import CardBingoSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(methods=['post'], detail=False)
    def cadastrar_evento(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.create_two_room(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def criar_sala(self, room):
        Room.objects.create(
            event_id=room['event_id'], minumum_quantity=room['minumum_quantity'], type=room['type']
        )

    def create_two_room(self, event_id):
        for i in range(1, 3):
            if i == 1:
                vip = {
                    'event_id': event_id,
                    'type': "V",
                    'minumum_quantity': 10,
                }
                self.criar_sala(vip)
            else:
                gratis = {
                    'event_id': event_id,
                    'type': "G",
                    'minumum_quantity': 5,
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
        if card.type == room.type and card.is_activate and card.price > 0:
            room.users.add(user)
            serializer = RoomSerializer(instance=room).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': {'message': "Ops, Você não tem permissão para entrar nessa sala!"}}, status=status.HTTP_401_UNAUTHORIZED)
