from flask import Blueprint, request, jsonify
from api.models import Role, User, Permission
from api import db
from api.auth.auth import auth_role_permission
from api.utils import json_failure, json_success
from flask_jwt_extended import jwt_required

roles = Blueprint("roles", __name__)


@roles.route("/roles", methods=["POST"])
def add_role():
    try:
        data = request.get_json()

        name_ = data["name"]
        slug_ = data["slug"]

        role = Role(name=name_, slug=slug_)

        role.insert()

        role_ = role.format()

        return jsonify({"role": role_}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@roles.route("/assign-role/<int:user_id>/<string:role_slug>", methods=["POST"])
def assign_role(user_id, role_slug):
    try:
        user = User.query.get(user_id)
        role = Role.query.filter_by(slug=role_slug).first()

        if user is None or role is None:
            return jsonify({"message": "User or role not found"}), 404

        user.roles.append(role)
        db.session.commit()

        return jsonify({"message": "Role assigned successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 422


@roles.route(
    "/assign-permission/<int:role_id>/<string:permission_slug>", methods=["POST"]
)
def assign_permission(role_id, permission_slug):
    try:
        role = Role.query.get(role_id)

        permission = Permission.query.filter_by(slug=permission_slug).first()

        if role is None or permission is None:
            return jsonify({"message": "role or permission not found"}), 404

        role.permissions.append(permission)

        db.session.commit()

        return jsonify({"message": "Permissions assigned successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 422


@roles.route("/roles/<int:role_id>", methods=["PUT"])
@jwt_required()
def update_role(role_id):
    try:
        data = request.get_json()

        role = Role.query.get(role_id)

        role.name = data["name"]
        role.slug = data["slug"]

        role.update()

        role_ = role.format()

        return json_success({"role": role_})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@roles.route("/roles/<int:role_id>", methods=["DELETE"])
def delete(role_id):
    try:
        role = Role.query.get(role_id)

        role.delete()

        role_ = role.format()

        return json_success({"role": role_})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@roles.route("/permissions", methods=["POST"])
def add_permission():
    try:
        data = request.get_json()

        name_ = data["name"]
        slug_ = data["slug"]

        permission = Permission(name=name_, slug=slug_)

        permission.insert()

        permission_ = permission.format()

        return jsonify({"permission": permission_}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})
