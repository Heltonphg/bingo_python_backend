from rest_framework import viewsets

from apps.users.models import User, CardBingo
from apps.users.serializers import UserSerializer, CardBingoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CardBingoViewSet(viewsets.ModelViewSet):
    queryset = CardBingo.objects.all()
    serializer_class = CardBingoSerializer