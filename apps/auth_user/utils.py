from apps.auth_user.serializers import UserAuthSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'user': UserAuthSerializer(user, context={'request': request}).data,
        'token': token,
    }
