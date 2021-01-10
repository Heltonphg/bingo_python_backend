from rest_framework import serializers

from api.serializers import PrimaryKeyNestedMixin
from apps.auth_user.models import User
from apps.auth_user.serializers import UserSimpleSerializer
from apps.card.models import CardBingo
from apps.core.models import Room
from apps.core.serializers import RoomSerializer


class CardBingoSimpleSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = CardBingo
        fields = (
            'id', 'user', 'room', 'is_activate', 'price'
        )

    def get_room(self, instance):
        return "{}".format(instance.room.id)

    def get_user(self, instance):
        return "{}".format(instance.user.id)


class CardBingoCadastroSerializer(serializers.ModelSerializer):
    room = PrimaryKeyNestedMixin(queryset=Room.objects.all(), serializer=RoomSerializer, required=False,
                                 allow_empty=True, allow_null=True)
    user = PrimaryKeyNestedMixin(queryset=User.objects.all(), serializer=UserSimpleSerializer, required=False,
                                 allow_empty=True, allow_null=True)
    cartelao = serializers.JSONField()

    class Meta:
        model = CardBingo
        fields = (
            'id', 'user', 'room', 'cartelao', 'is_activate', 'price'
        )


class MyCartelaoSerializer(serializers.ModelSerializer):
    cartelao = serializers.JSONField()

    class Meta:
        model = CardBingo
        fields = (
            'id', 'cartelao',
        )
