from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.auth_user.models import User
from apps.auth_user.serializers import UserAuthSerializer, UserSimpleSerializer


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def cadastrar(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
