def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'nickname': user.nickname,
        'is_superuser': user.is_superuser,
    }
