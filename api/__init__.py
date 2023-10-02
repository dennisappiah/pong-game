from flask import Flask, jsonify
from api.config import Config
from api.extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

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
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )

        return response

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"error": 404, "message": "The requested resource was not found."}),
            404,
        )

    @app.errorhandler(422)
    def un_processable(error):
        return (
            jsonify({"error": 422, "message": "Your request was un-processable."}),
            404,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": 500, "message": "Internal server error."})

    return app
