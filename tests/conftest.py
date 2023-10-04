import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from api.extensions import db, jwt
from api import config_by_name
from api.models import User


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config.from_object(config_by_name["testing"])

    db.init_app(app)
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

    # set-up
    with app.app_context():
        db.create_all()
        yield app  # Tests run here
        db.session.remove()
        db.drop_all()  # tear-down


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def test_user(app):
    # test user inserted into database
    with app.app_context():
        test_user = User(
            username="testuser", email="testuser@example.com", password="password"
        )
        db.session.add(test_user)
        db.session.commit()
        yield test_user


@pytest.fixture(scope="module")
def authenticated_client(client, test_user):
    access_token = create_access_token(identity=test_user.username)

    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    client_with_auth = client
    client_with_auth.environ_base["HTTP_AUTHORIZATION"] = headers["Authorization"]

    return client_with_auth
