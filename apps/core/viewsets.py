from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Event, Room
from apps.core.serializers import EventSerializer, RoomSerializer
from apps.users.models import User


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['post'], detail=True)
    def entrar(self, request, pk):
        usuario = self.request.data.get('usuario')
        room = Room.objects.get(id=pk)
        room.users.add(User.objects.get(id=usuario))
        serializer = RoomSerializer(instance=room).data
        return Response(serializer, status=status.HTTP_201_CREATED)
