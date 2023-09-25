from flask import Blueprint, request, abort, jsonify
from sqlalchemy import desc
from quickie.models import Leaderboard
from quickie.utils import paginator

leaderboard = Blueprint("leaderboard", __name__)


@leaderboard.route("/leaderboard")
def get_leaderboard_scores():
    results = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
    paginated_results = paginator(request, results)
    return jsonify({"results": paginated_results, "totalResults": len(results)})


@leaderboard.route("/leaderboard", methods=["POST"])
def post_to_leaderboard():
    try:
        player = request.get_json()["player"]
        score = int(request.get_json()["score"])

        board_item = Leaderboard(player=player, score=score)
        board_item.insert()

        return jsonify({"added": board_item.id, "success": True})
    except:
        abort(400)
