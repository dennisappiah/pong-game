from flask import request, current_app, abort
import jwt
from functools import wraps
from quickie.models import User


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            raise AuthError(
                {
                    "code": "authorization_header_missing",
                    "description": "Authorization header is expected.",
                },
                401,
            )
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.get(data["user_id"])
            if current_user is None:
                raise AuthError(
                    {
                        "code": "authorization_header_missing",
                        "description": "Authorization header is expected.",
                    },
                    401,
                )
            if not current_user["active"]:
                abort(403)
        except:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Authorization header must be bearer token.",
                },
                401,
            )
        return f(current_user, *args, **kwargs)

    return decorated
