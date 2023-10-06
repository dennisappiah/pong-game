from api.models import User, Role
from api import bcrypt, db
from api.utils import json_failure
from api.utils import save_image, allowed_file
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
    unset_jwt_cookies,
    set_access_cookies,
)

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["POST"])
def register_user_and_assign_roles():
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

        return make_response(jsonify(user=serialized_user), 201)

    except Exception as ex:
        db.session.rollback()
        return jsonify({"exception": str(ex)})


@users.route("/users/login", methods=["POST"])
def login_user():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        # confirming user exists before authentication
        user = User.query.filter_by(username=username).first()
        if not user:
            response_data = {"message": "Invalid username or password"}
            return make_response(jsonify(response_data), 400)

        valid_password = bcrypt.check_password_hash(user.password, password)
        if not valid_password:
            response_data = {"message": "Invalid username or password"}
            return make_response(jsonify(response_data), 400)

        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=user)

        # assign cookie-session-id
        set_access_cookies(response, access_token)

        return response

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@users.route("/me", methods=["GET", "POST"])
@jwt_required()
def retrieve_and_update_current_user():
    if request.method == "GET":
        return jsonify(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            image_file=current_user.file,
        )

    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        image_file_to_upload = request.files["file"]

        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if image_file_to_upload and allowed_file(image_file_to_upload.filename):
            optimized_image = save_image(image_file_to_upload)
            current_user.file = optimized_image

        db.session.commit()

        response_data = dict(
            message="profile updated successfully", file=optimized_image
        )

        return jsonify(response_data)


@users.route("/users/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


# account verification link (by email)
# forget-password & reset-password (by email)
