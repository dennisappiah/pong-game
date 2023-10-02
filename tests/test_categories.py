class TestGetCategories:
    def test_if_get_categories_returns_200(self, client):
        response = client.get("api/categories")  # act
        assert response.status_code == 200  # assert
