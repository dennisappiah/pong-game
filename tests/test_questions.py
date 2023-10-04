import json


class TestGetQuestions:
    def test_if_get_questions_returns_200(self, authenticated_client):
        response = authenticated_client.get("api/questions")

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] == True
        assert data["total_questions"] == 0

    def test_if_no_valid_question_route_returns_404(self, client):
        response = client.get("api/questions/20/y")

        assert response.status_code == 404
