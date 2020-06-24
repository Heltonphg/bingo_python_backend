from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','email',
            'full_name', 'nick_name',
            'cpf', 'phone', 'birth_date',
            'sex', 'avatar', 'created_at', 'updated_at']
