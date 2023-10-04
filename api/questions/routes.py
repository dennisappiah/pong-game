from flask import Blueprint, jsonify, request
from api.models import Question
from api.utils import paginator
from api.utils import json_failure, json_success, json_404
from flask_jwt_extended import jwt_required


questions = Blueprint("questions", __name__)


@questions.route("/questions", methods=["GET"])
@jwt_required()
def get_questions():
    try:
        questions_ = Question.query.all()
        paginated_questions = paginator(request, questions_)

        return json_success(
            {"questions": paginated_questions, "total_questions": len(questions_)}
        )

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@questions.route("/questions", methods=["POST"])
@jwt_required()
def add_question_or_search_question():
    try:
        data = request.get_json()
        search_term = data.get("searchTerm", None)

        if search_term is not None:
            search_pattern = f"%{search_term}%"

            questions_ = Question.query.filter(
                Question.question.ilike(search_pattern)
            ).all()

            formatted_questions = [question.format() for question in questions_]

            return json_success(
                {
                    "questions": formatted_questions,
                    "totalQuestions": len(questions_),
                    "currentCategory": None,
                }
            )
        else:
            question = data["question"]
            answer = data["answer"]
            difficulty = int(data["difficulty"])
            category_id = int(data["category_id"])

            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category_id=category_id,
            )

            question.insert()

            serialized_question = question.format()
            return jsonify({"question": serialized_question}), 201

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@questions.route("/questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return json_404(
                {"message": "The question with the given ID was not found!"}
            )

        question.delete()

        serialized_question = question.format()

        return json_success({"question": serialized_question})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@questions.route("/questions/<int:question_id>", methods=["GET"])
@jwt_required()
def retrieve_question(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return json_404(
                {"message": "The question with the given ID was not found!"}
            )

        serialized_question = question.format()

        return json_success({"question": serialized_question})

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@questions.route("/questions/<int:question_id>", methods=["PUT"])
@jwt_required()
def update_question(question_id):
    try:
        question = Question.query.get(question_id)

        if not question:
            return json_404(
                {"message": "The question with the given ID was not found!"}
            )

        data = request.get_json()

        question.question = data["question"]
        question.answer = data["answer"]
        question.difficulty = data["difficulty"]
        question.category_id = data["category_id"]

        question.update()

        serialized_question = question.format()

        return json_success({"question": serialized_question})

    except Exception as ex:
        return json_failure({"exception": str(ex)})
