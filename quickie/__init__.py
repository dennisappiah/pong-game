from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from quickie.config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from quickie.questions.routes import questions
    from quickie.categories.routes import categories

    app.register_blueprint(questions, url_prefix="/api")
    app.register_blueprint(categories, url_prefix="/api")

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

    with app.app_context():
        db.create_all()

    return app
