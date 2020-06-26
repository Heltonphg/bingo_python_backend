from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    cartela = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id','email', 'cartela',
            'full_name', 'nick_name',
            'cpf', 'phone', 'birth_date',
            'sex', 'avatar', 'created_at', 'updated_at')

    def get_cartela(self, instance):
        retorno = {
            "teste": instance.email
        }
        return retorno
        #instance.caaateeerlass.filllter(is_aticve=True)
