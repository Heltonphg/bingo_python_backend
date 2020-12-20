from rest_framework import serializers

from apps.auth_user.models import User
from apps.core.models import Room


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'nick_name', 'avatar', 'phone', 'sex')


class UserAuthSerializer(serializers.ModelSerializer):
    class _WinSerializer(serializers.Serializer):
        room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        price = serializers.DecimalField(max_digits=12, decimal_places=2)

    wins = _WinSerializer(many=True)

    cards = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password',
                  'nick_name', 'cards', 'cpf', 'phone',
                  'birth_date', 'sex', 'avatar', 'wins', 'valor_para_receber',
                  ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_cards(self, instance):
        try:
            retorno = instance.cards.get(user_id=instance.id, is_activate=True)
            data = [
                {
                    'id': retorno.id,
                    'price': retorno.price,
                    'ativo': retorno.is_activate,
                    'room_id': retorno.room.pk
                }
            ]
            return data

        except:
            return None