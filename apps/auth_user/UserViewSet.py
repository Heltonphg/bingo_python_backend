from rest_framework import viewsets

from apps.auth_user.models import User
from apps.auth_user.serializers import UserAuthSerializer


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer
