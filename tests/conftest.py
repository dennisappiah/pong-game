import pytest
from api import create_app, db
from pathlib import Path
import json

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
    def do_authenticate():
        resp_register = client.post(
            "api/users/register",
            data=json.dumps(
                dict(
                    username="joe",
                    email="joe@gmail.com",
                    password="123456",
                    is_staff=True,
                    is_super_admin=True,
                )
            ),
            content_type="application/json",
        )

        response = client.get(
            "api/users/me",
            headers=dict(
                Authorization="Bearer "
                + json.loads(resp_register.data.decode())["auth_token"]
            ),
        )

        data = json.loads(response.data.decode())

        assert ["data"] is not None
        assert response.status_code == 200
        assert data["status"] == "success"

    return do_authenticate
