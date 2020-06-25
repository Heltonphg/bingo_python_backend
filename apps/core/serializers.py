from rest_framework import serializers

from apps.core.models import Event, Room
from apps.users.models import User
from apps.users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'is_activated')


class RoomSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=False)
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Room
        fields = ('id', 'event', 'users', 'type',
                  'premium_price', 'initiation_game',
                  'minumum_quantity',
                  'created_at',
                  'updated_at')
