from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quickie.config import Config
from flask_cors import CORS
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from quickie.questions.routes import questions
    from quickie.categories.routes import categories
    from quickie.quizzes.routes import quizzes
    from quickie.users.routes import users

    app.register_blueprint(questions, url_prefix="/api")
    app.register_blueprint(categories, url_prefix="/api")
    app.register_blueprint(quizzes, url_prefix="/api")
    app.register_blueprint(users, url_prefix="/api")

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
    def unprocessable(error):
        return (
            jsonify({"error": 422, "message": "Your request was unprocessable."}),
            404,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": 400, "message": "Bad request."}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": 500, "message": "Internal server error."})

    with app.app_context():
        db.create_all()

    return app
