from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Event, Room
from apps.core.serializers import EventSerializer, RoomSerializer
from apps.users.models import User


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
                    'type': "Vip",
                    'minumum_quantity': 10,
                }
                self.criar_sala(vip)
            else:
                gratis = {
                    'event_id': event_id,
                    'type': "Grátis",
                    'minumum_quantity': 5,
                }
                self.criar_sala(gratis)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        user = self.request.data.get('user')
        if (user):
            room = Room.objects.get(id=pk)
            room.users.add(User.objects.get(id=user))
            serializer = RoomSerializer(instance=room).data
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response("Usuário não existe", status=status.HTTP_204_NO_CONTENT)
