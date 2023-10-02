from flask import Blueprint, request, jsonify
from api.models import Category, Question
from api.auth.auth import auth_role_permission
from flask_jwt_extended import jwt_required
from api.utils import json_failure, json_success, json_404


categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
# @jwt_required()
# @auth_role_permission("admin", "view_category")
def get_categories():
    try:
        categories_ = [category.format() for category in Category.query.all()]

        return json_success({"categories": categories_})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@categories.route("/categories", methods=["POST"])
# @jwt_required()
# @auth_role_permission("admin", "add_category")
def add_category():
    try:
        data = request.get_json()["type"]

        category = Category(type=data)
        category.insert()

        serialized_category = category.format()

        return jsonify({"category": serialized_category}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@categories.route("/categories/<int:category_id>/questions")
# @jwt_required()
def get_questions_in_category(category_id):
    try:
        questions = Question.query.filter_by(category_id=category_id).all()
        serialized_questions = [question.format() for question in questions]

        return json_success(
            {
                "questions": serialized_questions,
                "totalQuestions": len(questions),
            }
        )

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@categories.route("/categories/<int:category_id>", methods=["DELETE"])
# @jwt_required()
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return json_404(
                {"message": "The category with the given ID was not found!"}
            )

        category.delete()

        serialized_category = category.format()

        return json_success({"category": serialized_category})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@categories.route("/categories/<int:category_id>", methods=["PUT"])
# @jwt_required()
def update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return json_404(
                {"message": "The category with the given ID was not found!"}
            )

        data = request.get_json()["type"]
        category.type = data

        category.update()

        serialized_category = category.format()

        return json_success({"category": serialized_category})

    except Exception as ex:
        return json_failure({"exception": str(ex)})
