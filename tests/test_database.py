import pytest
from pathlib import Path

BASE_DIR = Path.cwd()
test_path = BASE_DIR.joinpath("test.db")


class TestDatabase:
    @pytest.mark.skipif
    def test_database(client):
        tester = test_path.is_file()
        assert tester
