from flask_jwt_extended import get_current_user
from functools import wraps
from flask import make_response
from dotenv import load_dotenv

load_dotenv()


def auth_role_permission(role, permission):
    def wrapper(fn):
        @wraps(fn)
        def decorated_route(*args, **kwargs):
            current_user = get_current_user()

            # ensure 'role' is a list, even if it's a single string.
            roles = role if isinstance(role, list) else [role]
            permissions = permission if isinstance(permission, list) else [permission]

            # Check if the user has all the required roles.
            if all(not current_user.has_role(r) for r in roles):
                return make_response(
                    {"msg": f"Missing any of roles {','.join(roles)}"}, 403
                )

            # Check if the user has all the required permissions.
            if all(not current_user.has_permission(p) for p in permissions):
                return make_response(
                    {"msg": f"Missing any of permissions {','.join(permissions)}"}, 403
                )

            # If the user has all required roles, call the original route function.
            return fn(*args, **kwargs)

        return decorated_route

    return wrapper
