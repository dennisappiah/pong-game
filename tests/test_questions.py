import json
import pytest


class TestCreateQuestion:
    def test_if_question_is_valid_returns_201(self, authenticated_client):
        request_data = {
            "question": "Who is the president of Ghana?",
            "answer": "Nana-Addo",
            "difficulty": 1,
            "category_id": 1,
        }

        response = authenticated_client.post(
            "/api/questions",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 201

    @pytest.mark.skipif
    def test_if_data_is_invalid_returns_400(self, authenticated_client):
        request_data = {
            "question": "Test question?",
            "answer": "Nana-Addo",
            "difficulty": True,
            "category_id": True,
        }

        response = authenticated_client.post(
            "/api/categories",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["type"] is not None


class TestGetQuestion:
    def test_if_get_questions_returns_200(self, authenticated_client):
        response = authenticated_client.get("api/questions")

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] == True
        assert data["total_questions"] == 1

    def test_if_no_valid_question_route_returns_404(self, client):
        response = client.get("api/questions/20/y")

        assert response.status_code == 404
