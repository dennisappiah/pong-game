from flask import Blueprint, request
from api.models import Question
import random
from flask_jwt_extended import jwt_required
from api.utils import json_failure, json_success


quizzes = Blueprint("quizzes", __name__)


@quizzes.route("/quizzes", methods=["POST"])
@jwt_required()
def get_question_for_quiz():
    try:
        """
        Endpoint to get questions to play the quiz.

        This endpoint takes category and previous question parameters
        and returns a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """
        data = request.get_json()

        previous_questions = data["previous_questions"]
        quiz_category = data["quiz_category"]

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

        return json_success({"question": question})

    except Exception as ex:
        return json_failure({"exception": str(ex)})
