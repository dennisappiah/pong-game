from flask import Blueprint, request, abort, jsonify
from api.models import Question
import random

quizzes = Blueprint("quizzes", __name__)


@quizzes.route("/quizzes", methods=["POST"])
def get_question_for_quiz():
    """
    Endpoint to get questions to play the quiz.

    This endpoint takes category and previous question parameters
    and returns a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    data = request.get_json()
    try:
        previous_questions = data["previous_questions"]
        quiz_category = data["quiz_category"]
    except:
        abort(400)

    if quiz_category:
        questions = (
            Question.query.filter_by(category_id=quiz_category)
            .filter(Question.id.notin_(previous_questions))
            .all()
        )
    else:
        questions = Question.query.filter(
            ~Question.category_id.in_(previous_questions)
        ).all()
    question = random.choice(questions).format() if questions else None

    return jsonify({"question": question})
