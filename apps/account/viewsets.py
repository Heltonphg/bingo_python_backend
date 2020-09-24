from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.models import Account
from apps.account.serializers import AccoutSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccoutSerializer
    queryset = Account.objects.all()

    @action(methods=['get'], detail=False)
    def minha(self, request):
        account = Account.objects.filter(user=request.user).first()
        if not account:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        serializer = AccoutSerializer(instance=account).data
        return Response(serializer, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def criar(self, request):
        account = Account.objects.create(user_id=request.user.id,
                                         nome=request.data['nome'],
                                         cpf=request.data['cpf'],
                                         tipo=request.data['tipo'],
                                         banco=request.data['banco'],
                                         conta=request.data['conta'], validade=request.data['validade'],
                                         agencia=request.data['agencia'])
        serializer = AccoutSerializer(instance=account).data
        return Response(serializer, status=status.HTTP_201_CREATED)
