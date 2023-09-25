from flask import Blueprint, jsonify, request, abort
from quickie.models import Category, Question
from .utils import serialize_category
from quickie.auth.auth_middleware import token_required

categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
@token_required
def get_categories():
    categories_ = [serialize_category(category) for category in Category.query.all()]

    return jsonify({"categories": categories_}), 200


@categories.route("/categories", methods=["POST"])
def add_category():
    try:
        data = request.get_json()["type"]

        category = Category(type=data)
        category.insert()

        serialized_category = serialize_category(category)

        return jsonify({"category": serialized_category}), 201
    except:
        abort(400)


@categories.route("/categories/<int:category_id>/questions")
def get_questions_in_category(category_id):
    questions = Question.query.filter_by(category_id=category_id).all()
    formatted_questions = [question.format() for question in questions]

    return (
        jsonify(
            {
                "questions": formatted_questions,
                "totalQuestions": len(questions),
            }
        ),
        200,
    )


@categories.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)

    try:
        category.delete()

        serialized_category = serialize_category(category)

        return jsonify({"category": serialized_category}), 200
    except:
        abort(422)


@categories.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)

    try:
        data = request.get_json()["type"]
        category.type = data

        category.update()

        serialized_category = serialize_category(category)

        return jsonify({"category": serialized_category}), 200
    except:
        abort(422)
