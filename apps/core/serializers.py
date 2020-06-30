from rest_framework import serializers

from apps.core.models import Bingo, Room
from apps.users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    bingo = serializers.SerializerMethodField()
    users = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'bingo', 'users', 'type',
                  'premium_price','value_card', 'initiation_game',
                  'minumum_quantity',
                  'created_at',
                  'updated_at'
                  )

    def get_bingo(self, instance):
        return "{} ({})".format(instance.bingo.name, instance.type)


class BingoSerializer(serializers.ModelSerializer):
    roons = RoomSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Bingo
        fields = ('id', 'name', 'roons', 'time_initiation', 'is_activated')
