from flask import Blueprint, jsonify, request, abort
from quickie.models import Category, Question
from .utils import serialize_category

categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
def get_categories():
    categories_ = [serialize_category(category) for category in Category.query.all()]

    return jsonify({"categories": categories_})


@categories.route("/categories", methods=["POST"])
def add_category():
    try:
        data = request.get_json()["type"]

        category = Category(type=data)
        category.insert()

        serialized_category = serialize_category(category)

        return jsonify({"category": serialized_category})
    except:
        abort(400)


@categories.route("/categories/<int:category_id>/questions")
def get_questions_in_category(category_id):
    questions = Question.query.filter_by(category_id=category_id).all()
    formatted_questions = [question.format() for question in questions]

    return jsonify(
        {
            "questions": formatted_questions,
            "totalQuestions": len(questions),
        }
    )
