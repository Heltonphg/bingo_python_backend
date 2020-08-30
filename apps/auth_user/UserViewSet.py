from django.utils import timezone
from django.core.mail import send_mail
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

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def recuperar_senha(self, request, *args, **kwargs):
        resh = 'sdsakdf'
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response('Usuário não encontrado', status=status.HTTP_400_BAD_REQUEST)
        user.token = resh
        user.token_created_at = timezone.now()
        user.save()
        send_mail('Solicitação de recuperação de senha',
                  'Olá {}, segue o código para recuperação da senha: {}'.format(user.nick_name, resh), None,
                  [request.data['email']])
        return Response('Email enviado', status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def resetar_senha(self, request, *args, **kwargs):
        user = User.objects.filter(token=request.data['token']).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
        else:
            return Response('Token inválido.', status=status.HTTP_400_BAD_REQUEST)
        return Response('Senha atualizada', status=status.HTTP_201_CREATED)
