from flask import Blueprint, jsonify, request, abort
from quickie.models import Category


categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=["GET"])
def get_categories():
    categories_ = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories_}

    return jsonify({"categories": formatted_categories})


@categories.route("/categories", methods=["POST"])
def add_category():
    try:
        data = request.get_json()
        type_ = data["type"]
        category = Category(type=type_)
        category.insert()

        return jsonify({"added": category.id, "success": True})
    except:
        abort(400)
