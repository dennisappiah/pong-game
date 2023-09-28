from functools import wraps
from flask import make_response
from flask_jwt_extended import get_current_user


def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_route(*args, **kwargs):
            current_user = get_current_user()

            # ensure 'role' is a list, even if it's a single string.
            roles = role if isinstance(role, list) else [role]

            # Check if the user has all the required roles.
            if all(not current_user.has_role(r) for r in roles):
                return make_response(
                    {"msg": f"Missing any of roles {','.join(roles)}"}, 403
                )

            # If the user has all required roles, call the original route function.
            return fn(*args, **kwargs)

        return decorated_route

    return wrapper
