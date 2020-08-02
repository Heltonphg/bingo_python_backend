from rest_framework import serializers

from apps.auth_user.models import User

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id', 'email', 'full_name', 'nick_name', 'avatar', 'phone')

class UserAuthSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password',
            'nick_name', 'cards',  'cpf',  'phone',
            'birth_date', 'sex', 'avatar',
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
