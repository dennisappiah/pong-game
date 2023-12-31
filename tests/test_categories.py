import pytest
import json


class TestCreateCategory:
    def test_if_category_is_valid_returns_201(self, authenticated_client):
        request_data = {"type": "a"}

        response = authenticated_client.post(
            "/api/categories",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 201

    @pytest.mark.skipif
    def test_if_user_is_anonymous_returns_401(self, client):
        request_data = {"type": "a"}

        response = client.post(
            "/api/categories",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 401


class TestGetCategory:
    def test_if_get_categories_returns_200(self, authenticated_client):
        response = authenticated_client.get("/api/categories")  # act

        assert response.status_code == 200  # assert
        data = json.loads(response.data)
        assert data["success"] == True

    def test_if_get_questions_by_categories_returns_200(self, authenticated_client):
        response = authenticated_client.get("/api/categories/1/questions")

        assert response.status_code == 200

    def test_if_categories_exists_return_200(self, authenticated_client):
        response = authenticated_client.get("/api/categories/1")

        assert response.status_code == 200


class TestDeleteCategory:
    def test_if_delete_category_returns_200(self, authenticated_client):
        response = authenticated_client.delete("/api/categories/1")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] == True

    def test_if_wrong_delete_operation_returns_405(self, authenticated_client):
        response = authenticated_client.post("/api/categories/1")

        assert response.status_code == 405
