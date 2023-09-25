from flask import request, current_app, abort
import jwt
from functools import wraps
from quickie.models import User


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def extract_token_from_header(auth_header):
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = extract_token_from_header(request.headers.get("Authorization"))
        if not token:
            raise AuthError(
                {
                    "code": "authorization_header_missing",
                    "description": "Authorization header is missing or invalid.",
                },
                401,
            )
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            if user_id is None:
                raise AuthError(
                    {"code": "invalid_token", "description": "Invalid token format."},
                    401,
                )
            current_user = User.query.get(int(user_id))
            if current_user is None:
                raise AuthError(
                    {
                        "code": "unauthorized_user",
                        "description": "User not authorized.",
                    },
                    403,
                )
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token has expired."},
                401,
            )
        except jwt.InvalidTokenError:
            raise AuthError(
                {"code": "invalid_token", "description": "Invalid token."},
                401,
            )
        return f(current_user, *args, **kwargs)

    return wrapper
