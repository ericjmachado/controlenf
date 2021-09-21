

def jwt_response_payload_handler(token, user=None, request=None):
    from core.api.v1.serializers import UserSerializer

    user_data = UserSerializer(user).data

    return {
        "user": user_data,
        "token": token,
    }

