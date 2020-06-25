from rest_framework import viewsets
from rest_framework.decorators import action
from apps.core.models import Event, Room
from apps.core.serializers import EventSerializer, RoomSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

