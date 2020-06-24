from rest_framework import serializers
from apps.core.models import Event, Room


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'is_activated']

class RoomSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = Room
        fields = ['id','event', 'type',
                  'premium_price', 'initiation_game',
                  'minumum_quantity',
                  'created_at',
                  'updated_at']