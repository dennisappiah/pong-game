from flask import Blueprint, request, abort, jsonify, current_app
from quickie.models import User
from quickie import bcrypt
from .utils import serialize_user
import jwt

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

        serialized_user = serialize_user(user)
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
            abort(400)

        valid_password = bcrypt.check_password_hash(user.password, password)
        if not valid_password:
            abort(400)

        # generate jwt token
        payload = {
            "user_id": user.id,
            "email": user.email,
        }

        jwt_token = jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

        return jsonify({"token": jwt_token})
    except:
        abort(400)
