from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from api.models import Leaderboard
from api.utils import paginator
from api.utils import json_failure, json_success


leaderboard = Blueprint("leaderboard", __name__)


@leaderboard.route("/leaderboard")
@jwt_required()
def get_leaderboard_scores():
    try:
        results = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
        paginated_results = paginator(request, results)
        return json_success(
            {"results": paginated_results, "totalResults": len(results)}
        )

    except Exception as ex:
        return json_failure({"exception": str(ex)})


@leaderboard.route("/leaderboard", methods=["POST"])
def post_to_leaderboard():
    try:
        player = request.get_json()["player"]
        score = int(request.get_json()["score"])

        board_item = Leaderboard(player=player, score=score)
        board_item.insert()

        return json_success({"board_item": board_item.format()})

    except Exception as ex:
        return json_failure({"exception": str(ex)})
