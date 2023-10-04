from flask import Blueprint, request, jsonify, make_response
from api.models import User, Role
from api import bcrypt, db
from api.utils import json_failure
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
    create_refresh_token,
)

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["POST"])
def register_users_and_assign_roles():
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

        db.session.add(user)

        if data.get("is_staff"):
            admin_role = Role.query.filter_by(slug="admin").first()
            user.roles.append(admin_role)
            user.is_staff = True
        if data.get("is_super_admin"):
            super_admin_role = Role.query.filter_by(slug="super-admin").first()
            user.roles.append(super_admin_role)
            user.is_super_admin = True

        db.session.commit()

        serialized_user = user.format()

        access_token = create_access_token(identity=user)

        return (
            jsonify({"user": serialized_user, "access_token": access_token}),
            201,
        )

    except Exception as ex:
        db.session.rollback()
        return json_failure({"exception": str(ex)})


@users.route("/users/login", methods=["POST"])
def login_user():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        # confirming user exists before authentication
        user = User.query.filter_by(username=username).one_or_none()
        if not user:
            response_data = {"message": "Invalid username or password"}
            return make_response(jsonify(response_data), 400)

        valid_password = bcrypt.check_password_hash(user.password, password)
        if not valid_password:
            response_data = {"message": "Invalid username or password"}
            return make_response(jsonify(response_data), 400)

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return jsonify({"access_token": access_token, "refresh_token": refresh_token})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@users.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )
