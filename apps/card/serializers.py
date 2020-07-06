from rest_framework import serializers

from apps.auth_user.serializers import UserAuthSerializer
from apps.card.models import CardBingo


class CardBingoSerializer(serializers.ModelSerializer):
    user = UserAuthSerializer(many=False)
    card = serializers.JSONField()

    class Meta:
        model = CardBingo
        fields = (
            'user', 'card', 'is_activate', 'price'
        )
