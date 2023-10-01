from flask import Blueprint, request, jsonify, current_app, make_response
from api.models import User
from api import bcrypt
import jwt
from api.auth.auth import auth_role_permission
from flask_jwt_extended import jwt_required
from api.utils import json_failure

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json()

        username = data["username"]
        email = data["email"]
        password = data["password"]

        # checking if  user is  already registered
        user = User.query.filter_by(username=username, email=email).first()
        if user is not None:
            response_data = {"message": "User is already registered"}
            return make_response(jsonify(response_data), 400)

        user = User(username=username, email=email, password=password)
        user.password = bcrypt.generate_password_hash(user.password).decode("utf-8")

        user.insert()

        serialized_user = user.format()
        return jsonify({"user": serialized_user}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@users.route("/users/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            response_data = {"message": "Invalid email or password"}
            return make_response(jsonify(response_data), 400)

        valid_password = bcrypt.check_password_hash(user.password, password)
        if not valid_password:
            response_data = {"message": "Invalid email or password"}
            return make_response(jsonify(response_data), 400)

        roles = [role.slug for role in user.roles]

        # generate jwt token
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "email": user.email,
            "roles": roles,
        }

        jwt_token = jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

        return jsonify({"token": jwt_token}), 200

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@users.route("/users")
@jwt_required()
@auth_role_permission("admin", "view_users")
def get_users():
    try:
        users_ = [user.format() for user in User.query.all()]

        return jsonify({"users": users_, "total_users": len(users_)})

    except Exception as ex:
        return json_failure({"exception": str(ex)})
