from core.api.v1.serializers import LoginSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user_data = LoginSerializer(user).data

    return {
        **user_data,
        "token": token,
    }

