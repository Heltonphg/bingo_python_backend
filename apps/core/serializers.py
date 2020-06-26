from rest_framework import serializers

from apps.core.models import Event, Room
from apps.users.serializers import UserSerializer


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


class EventSerializer(serializers.ModelSerializer):
    roons = RoomSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'roons', 'time_initiation', 'is_activated')
