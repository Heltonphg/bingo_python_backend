from apps.auth_user.serializers import UserSimpleSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'user': UserSimpleSerializer(user, context={'request': request}).data,
        'token': token,
    }
