import pytest
import json


@pytest.fixture
def create_category(client):
    def do_create_category(category=None):
        return client.post("/api/categories", json={**category})

    return do_create_category


class TestGetCategories:
    @pytest.mark.skipif
    def test_if_get_categories_returns_200(self, client):
        response = client.get("/api/categories")  # act
        assert response.status_code == 200  # assert


class TestCreateCategory:
    def test_if_user_is_anonymous_returns_401(self, create_category):
        response = create_category({"type": "education"})
        assert response.status_code == 401

    @pytest.mark.skipif
    def test_if_user_not_admin_returns_403(self, authenticate, create_category):
        authenticate()

        response = create_category({"type": "a"})

        assert response.status_code == 403

    @pytest.mark.skipif
    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        authenticate()

        response = create_category({"type": ""})
        data = json.loads(response.data)
        assert response.status_code == 400
        assert data["type"] is not None

    def test_if_category_is_valid_returns_201(self, authenticate, create_category):
        authenticate()

        response = create_category({"type": "education"})
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data["id"] > 0


class TestRetrieveCollection:
    @pytest.mark.skipif
    def test_if_collection_exists_return_200(self, client):
        response = client.get("/api/categories/1")

        assert response.status_code == 200
