from rest_framework import viewsets

from apps.card.models import CardBingo
from apps.card.serializers import CardBingoSerializer


class CardBingoViewSet(viewsets.ModelViewSet):
    queryset = CardBingo.objects.all()
    serializer_class = CardBingoSerializer