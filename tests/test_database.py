import pytest
from pathlib import Path
import json

BASE_DIR = Path.cwd()
test_path = BASE_DIR.joinpath("test.db")


class TestDatabase:
    @pytest.mark.skipif
    def test_if_database_file_exists(self, client):
        tester = test_path.is_file()
        assert tester

    def test_if_database_is_empty(self, client):
        response = client.get("/")
        data = json.loads(response.data)

        assert response.status_code == 404
        assert data["message"] == "The requested resource was not found"
