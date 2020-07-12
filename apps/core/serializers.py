from rest_framework import serializers

from api.serializers import PrimaryKeyNestedMixin
from apps.auth_user.serializers import UserAuthSerializer
from apps.card.models import CardBingo
from apps.core.models import Bingo, Room

# class EntrarSalaSerializer(serializers.Serializer):
#     card = serializers.PrimaryKeyRelatedField(queryset=CardBingo.objects.filter(is_activate=True, u))
#     room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

class RoomSerializer(serializers.ModelSerializer):
    bingo = serializers.SerializerMethodField()
    users = UserAuthSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'bingo', 'users', 'type',
                  'valor_premio','value_card', 'initiation_game',
                  'minumum_quantity',
                  'created_at',
                  'updated_at'
                  )

    def get_bingo(self, instance):
        return "{} ({})".format(instance.bingo.name, instance.type)



class BingoSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Bingo
        fields = ('id', 'name', 'rooms', 'time_initiation', 'is_activated')



