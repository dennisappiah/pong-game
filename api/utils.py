from flask import jsonify

QUESTIONS_PER_PAGE = 5


def paginator(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start:end]


def json_failure(fields=None):
    if fields is None:
        fields = {}
    return jsonify({"success": False, **fields})


def json_success(fields=None):
    if fields is None:
        fields = {}
    return jsonify({"success": True, **fields}), 200


def json_404(fields=None):
    if fields is None:
        fields = {}
    return jsonify({"success": True, **fields}), 404
