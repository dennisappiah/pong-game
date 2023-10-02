# import pytest
# from api import create_app, db
# from tests.test_config import TestConfig
#
#
# @pytest.fixture()
# def app():
#     app = create_app()
#     app.config.from_object(TestConfig)
#
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.drop_all()
#
#
# @pytest.fixture()
# def client(app):
#     return app.test_client()
