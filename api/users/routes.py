from flask import Blueprint, request, abort, jsonify, current_app
from api.models import User
from api import bcrypt
import jwt
from api.utils import paginator
from api.auth.auth_role import auth_role
from flask_jwt_extended import jwt_required

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    try:
        username = data["username"]
        email = data["email"]
        password = data["password"]

        user = User(username=username, email=email, password=password)
        user.password = bcrypt.generate_password_hash(user.password).decode("utf-8")

        user.insert()

        serialized_user = user.format()
        return jsonify({"user": serialized_user}), 201
    except:
        abort(400)


@users.route("/users/login", methods=["POST"])
def login_user():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(400, "'Invalid email or password'")

        valid_password = bcrypt.check_password_hash(user.password, password)
        if not valid_password:
            abort(400, "'Invalid email or password'")

        # generate jwt token
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "email": user.email,
            "roles": user.roles,
        }

        jwt_token = jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

        return jsonify({"token": jwt_token})
    except:
        abort(400)


@users.route("/users")
@jwt_required()
@auth_role(["super_admin"])
def get_users():
    try:
        users_ = User.query.all()

        paginated_users = paginator(request, users_)

        return jsonify({"users": paginated_users, "total_users": len(users_)})
    except:
        abort(422)
