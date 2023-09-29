from flask import Blueprint, jsonify, request, abort
from api.models import Category, Question
from api.auth.auth_role import auth_role
from flask_jwt_extended import jwt_required


categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
@jwt_required()
@auth_role(["admin", "super-admin"])
def get_categories():
    categories_ = [category.format() for category in Category.query.all()]

    return jsonify({"categories": categories_}), 200


@categories.route("/categories", methods=["POST"])
@jwt_required()
@auth_role(["admin", "super-admin"])
def add_category():
    try:
        data = request.get_json()["type"]

        category = Category(type=data)
        category.insert()

        serialized_category = category.format()

        return jsonify({"category": serialized_category}), 201
    except:
        abort(400)


@categories.route("/categories/<int:category_id>/questions")
@jwt_required()
@auth_role(["admin", "super-admin"])
def get_questions_in_category(category_id):
    questions = Question.query.filter_by(category_id=category_id).all()
    serialized_questions = [question.format() for question in questions]

    return (
        jsonify(
            {
                "questions": serialized_questions,
                "totalQuestions": len(questions),
            }
        ),
        200,
    )


@categories.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
@auth_role(["admin", "super-admin"])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)

    try:
        category.delete()

        serialized_category = category.format()

        return jsonify({"category": serialized_category}), 200
    except:
        abort(422)


@categories.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
@auth_role(["admin", "super-admin"])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)

    try:
        data = request.get_json()["type"]
        category.type = data

        category.update()

        serialized_category = category.format()

        return jsonify({"category": serialized_category}), 200
    except:
        abort(422)
