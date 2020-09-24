from rest_framework import serializers

from api.serializers import PrimaryKeyNestedMixin
from apps.account.models import Account
from apps.auth_user.models import User
from apps.auth_user.serializers import UserSimpleSerializer


class AccoutSerializer(serializers.ModelSerializer):
    user = PrimaryKeyNestedMixin(queryset=User.objects.all(), serializer=UserSimpleSerializer, required=False,
                                 allow_empty=True, allow_null=True)

    class Meta:
        model = Account
        fields = ('id', 'user', 'conta', 'validade', 'agencia', 'nome', 'banco', 'cpf', 'tipo')
