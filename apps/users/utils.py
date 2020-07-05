from apps.users.serializers import UserSerializerSimple


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializerSimple(user, context={'request': request}).data
    }