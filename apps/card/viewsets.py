from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.card.models import CardBingo
from apps.card.serializers import CardBingoCadastroSerializer, MyCartelaoSerializer, CardBingoSimpleSerializer


class CardBingoViewSet(viewsets.ModelViewSet):
    queryset = CardBingo.objects.all()
    serializer_class = CardBingoSimpleSerializer

    @action(methods=['post'], detail=True)
    def cadastrar(self, request, pk):
        card = CardBingo.objects.filter(is_activate=True, user=request.user).first()
        if card:
            raise serializers.ValidationError('Você já possui uma cartela ativa.')
        else:
            data = {
                "user": request.user.pk,
                "room": pk,
                "cartelao": request.data['cartelao'],
                "price": request.data['price']
            }
            serializer = CardBingoCadastroSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def get_my_cartelao(self, request):
        card = CardBingo.objects.filter(is_activate=True, user=request.user).first()
        if not card:
            raise serializers.ValidationError('{},você ainda não possui nenhuma cartela.'.format(request.user))
        serializer = MyCartelaoSerializer(instance=card).data
        return Response(serializer, status=status.HTTP_200_OK)
