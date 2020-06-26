from rest_framework import serializers

from apps.core.models import Event, Room
from apps.users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'time_initiation','is_activated')


class RoomSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    users = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'event', 'users', 'type',
                  'premium_price', 'initiation_game',
                  'minumum_quantity',
                  'created_at',
                  'updated_at'
                  )

    def get_event(self, instance):
        return instance.event.name
