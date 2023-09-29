from flask import Blueprint, request, abort, jsonify
from api.models import Role, User
from api import db
from api.auth.auth_role import auth_role
from flask_jwt_extended import jwt_required

roles = Blueprint("roles", __name__)


@roles.route("/roles", methods=["POST"])
@jwt_required()
@auth_role(["super-admin"])
def add_role():
    data = request.get_json()

    try:
        name_ = data["name"]
        slug_ = data["slug"]

        role = Role(name=name_, slug=slug_)

        role.insert()

        role_ = role.format()

        return jsonify({"role": role_})
    except:
        abort(400)


@roles.route("/roles/<int:role_id>", methods=["PUT"])
@jwt_required()
@auth_role(["super-admin"])
def update_role(role_id):
    data = request.get_json()
    try:
        role = Role.query.get(role_id)

        role.name = data["name"]
        role.slug = data["slug"]

        role.update()

        role_ = role.format()

        return jsonify({"role": role_})
    except:
        abort(400)


@roles.route("/roles/<int:role_id>", methods=["DELETE"])
@jwt_required()
@auth_role(["super-admin"])
def delete(role_id):
    try:
        role = Role.query.get(role_id)

        role.delete()

        role_ = role.format()

        return jsonify({"role": role_})
    except:
        abort(422)


@roles.route("/assign-role/<int:user_id>/<string:role_slug>", methods=["POST"])
@jwt_required()
@auth_role(["super-admin"])
def assign_role(user_id, role_slug):
    try:
        user = User.query.get(user_id)
        role = Role.query.filter_by(slug=role_slug).first()

        if user is None or role is None:
            return jsonify({"message": "User or role not found"}), 404

        user.roles.append(role)
        db.session.commit()

        return jsonify({"message": "Role assigned successfully"}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 400
