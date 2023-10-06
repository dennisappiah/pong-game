from flask import jsonify, current_app
import secrets
import os
from PIL import Image
from flask_mail import Message

from api import mail

QUESTIONS_PER_PAGE = 5


def paginator(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start:end]


def save_image(image_path):
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(image_path.filename)

    new_image_name = random_hex + f_ext

    output_folder_path = os.path.join(
        current_app.root_path, "static/profile_pics", new_image_name
    )

    output_size = (200, 200)

    i = Image.open(image_path)
    i.thumbnail(output_size)
    i.save(output_folder_path)

    return new_image_name


def send_email(user, subject, sender, body):
    msg = Message(subject, sender=sender, recipients=[user.email])
    msg.body = body
    mail.send(msg)


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
