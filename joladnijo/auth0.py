import json
import os
from functools import wraps

import jwt
import requests
from django.contrib.auth import authenticate
from django.http import JsonResponse


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get(os.environ.get("JWT_KEYS")).json()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception("Public key not found.")

    return jwt.decode(
        token,
        public_key,
        audience=os.environ.get("JWT_AUDIENCE"),
        issuer=os.environ.get("JWT_ISSUER"),
        algorithms=[os.environ.get("JWT_ALGORITHM", "RS256")],
    )


def jwt_get_username_from_payload_handler(payload):
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header"""
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_permission(required_permission):
    """Determines if the required permission is present in the Access Token
    Args:
        required_permission (str): The permission required to access the resource
    """

    def require_permission(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("permissions"):
                permissions = decoded["permissions"]
                for permission in permissions:
                    if permission == required_permission:
                        return f(*args, **kwargs)
            response = JsonResponse({"message": "You don't have access to this resource"})
            response.status_code = 403
            return response

        return decorated

    return require_permission
