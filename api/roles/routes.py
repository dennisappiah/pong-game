from flask import Blueprint, request, jsonify
from api.models import Role, Permission
from api.utils import json_failure, json_success


roles = Blueprint("roles", __name__)


@roles.route("/roles", methods=["POST"])
def add_role_and_assign_permissions():
    try:
        data = request.get_json()

        name_ = data["name"]
        slug_ = data["slug"]
        permissions_slugs = data.get("permissions", [])

        role = Role(name=name_, slug=slug_)

        # Retrieve permissions based on permission slugs
        permissions = Permission.query.filter(
            Permission.slug.in_(permissions_slugs)
        ).all()

        # Assign the retrieved permissions to the role
        role.permissions.extend(permissions)

        role.insert()

        role_data = {
            "id": role.id,
            "name": role.name,
            "slug": role.slug,
            "permissions": [permission.slug for permission in permissions],
        }

        return jsonify({"role": role_data}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@roles.route("/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    try:
        data = request.get_json()

        role = Role.query.get(role_id)

        role.name = data["name"]
        role.slug = data["slug"]
        role.permissions = data["permissions"]

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
