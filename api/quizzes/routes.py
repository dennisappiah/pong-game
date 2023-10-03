from flask import Blueprint, request
from api.models import Question
import random
from api.utils import json_failure, json_success


quizzes = Blueprint("quizzes", __name__)


@quizzes.route("/quizzes", methods=["POST"])
def get_question_for_quiz(current_user):
    try:
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
