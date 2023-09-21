from flask import Blueprint, jsonify, request, abort
from quickie.models import Question
from .utils import paginator

questions = Blueprint("questions", __name__)


@questions.route("/questions", methods=["GET"])
def get_questions():
    questions_ = Question.query.all()
    paginated_questions = paginator(request, questions_)

    if not len(questions_):
        abort(404)
    return jsonify(
        {
            "questions": paginated_questions,
            "total_questions": len(questions_),
            "current_category": None,
        }
    )


@questions.route("/questions", methods=["POST"])
def add_question():
    """
    - Endpoint to add a new question and to get questions based on a search term.
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
            category = int(data["category"])

            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category,
            )

            question.insert()

            return jsonify({"added": question.id, "success": True})
    except:
        abort(400)
