import os
from flask import jsonify, current_app
from flask_mail import Message
from werkzeug.utils import secure_filename
from PIL import Image


from api import mail

QUESTIONS_PER_PAGE = 5


def paginator(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start:end]


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(image_file):
    try:
        new_image_name = secure_filename(image_file.filename)
        output_folder_path = os.path.join(
            current_app.root_path, "static/profile_pics", new_image_name
        )
        output_size = (200, 200)
        i = Image.open(image_file)
        i.thumbnail(output_size)
        i.save(output_folder_path)
        return new_image_name
    except Exception as e:
        return str(e)


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
