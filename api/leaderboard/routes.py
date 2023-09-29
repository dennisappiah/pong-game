from flask import Blueprint, request, abort, jsonify
from sqlalchemy import desc
from api.models import Leaderboard
from api.utils import paginator
from api.auth.auth_role import auth_role
from flask_jwt_extended import jwt_required

leaderboard = Blueprint("leaderboard", __name__)


@leaderboard.route("/leaderboard")
@jwt_required()
@auth_role(["admin", "super-admin"])
def get_leaderboard_scores():
    results = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
    paginated_results = paginator(request, results)
    return jsonify({"results": paginated_results, "totalResults": len(results)})


@leaderboard.route("/leaderboard", methods=["POST"])
@jwt_required()
@auth_role(["admin", "super-admin"])
def post_to_leaderboard():
    try:
        player = request.get_json()["player"]
        score = int(request.get_json()["score"])

        board_item = Leaderboard(player=player, score=score)
        board_item.insert()

        return jsonify({"added": board_item.format(), "success": True})
    except:
        abort(400)
