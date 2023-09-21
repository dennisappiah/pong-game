from flask import Blueprint, jsonify, request, abort
from quickie.models import Question, Category
from .utils import paginator, serialize_question

questions = Blueprint("questions", __name__)


@questions.route("/questions", methods=["GET"])
def get_questions():
    questions_ = Question.query.all()
    paginated_questions = paginator(request, questions_)

    if not len(questions_):
        abort(404)
    return jsonify(
        {"questions": paginated_questions, "total_questions": len(questions_)}
    )


@questions.route("/questions", methods=["POST"])
def add_question():
    """
    - Endpoint to add a new question and to retrieve questions based on a search term.
    - request.get_json() : Parses the incoming JSON request data and returns it.
    """
    try:
        data = request.get_json()
        search_term = data.get("searchTerm", None)

        if search_term is not None:
            search_pattern = f"%{search_term}%"
            questions_ = Question.query.filter(
                Question.question.ilike(search_pattern)
            ).all()
            formatted_questions = [question.format() for question in questions_]

            return jsonify(
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

            serialized_question = serialize_question(question)
            return jsonify({"question": serialized_question})
    except:
        abort(400)


@questions.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)

    try:
        question.delete()

        serialized_question = serialize_question(question)
        return jsonify({"question": serialized_question})
    except:
        abort(422)


@questions.route("/questions/<int:question_id>", methods=["GET"])
def retrieve_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)

    try:
        serialized_question = serialize_question(question)
        return jsonify({"question": serialized_question})
    except:
        abort(422)
