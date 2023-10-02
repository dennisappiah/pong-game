import pytest
from api import create_app, db
from pathlib import Path
from api.models import User

app = create_app()

TEST_DB = "test.db"


@pytest.fixture
def client():
    BASE_DIR = Path.cwd()
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR.joinpath(TEST_DB)}"

    # set-up
    with app.app_context():
        db.create_all()

    client = app.test_client()
    yield client  # Tests run here

    # tear-down
    with app.app_context():
        db.drop_all()


@pytest.fixture
def authenticate(client):
    def do_authenticate(is_staff=False):
        user = User(id=1, username="test_user", is_staff=is_staff)

        with client.session_transaction() as session:
            session["user_id"] = user.id
        return user

    return do_authenticate
