import json
from datetime import datetime, timezone, timedelta
from api.config import config_by_name
from api.extensions import db, migrate, jwt, bcrypt, mail
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
)


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from api.questions.routes import questions
    from api.categories.routes import categories
    from api.quizzes.routes import quizzes
    from api.users.routes import users
    from api.roles.routes import roles

    app.register_blueprint(questions, url_prefix="/api")
    app.register_blueprint(categories, url_prefix="/api")
    app.register_blueprint(quizzes, url_prefix="/api")
    app.register_blueprint(users, url_prefix="/api")
    app.register_blueprint(roles, url_prefix="/api")

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        # content-type multipart/form-data
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, enctype"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )

        return response

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    @app.errorhandler(404)
    def not_found(error):
        return make_response(
            jsonify(message="The requested resource was not found"), 404
        )

    @app.errorhandler(422)
    def un_processable(error):
        return make_response(jsonify(message="Your request was un-processable"), 422)

    @app.errorhandler(413)
    def too_large(e):
        return make_response(jsonify(message="File is too large"), 413)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify(message="Internal server error"), 500)

    return app
