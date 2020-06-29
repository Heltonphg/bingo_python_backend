from rest_framework import serializers

from apps.users.models import User, CardBingo


class UserSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'cards',
            'full_name', 'nick_name',
            'cpf', 'phone', 'birth_date',
            'sex', 'avatar', 'created_at', 'updated_at')

    def get_cards(self, instance):
        try:
            retorno = instance.cards.get(user_id=instance.id, is_activate=True)
            if retorno:
                data = [
                    {
                        'id': retorno.id,
                        'price': retorno.price,
                        'room_id': retorno.room.pk
                    }
                ]
                return data
        except:
            return None


class CardBingoSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    card = serializers.JSONField()

    class Meta:
        model = CardBingo
        fields = (
            'user', 'card', 'is_activate', 'price'
        )
