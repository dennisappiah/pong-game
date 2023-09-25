import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"  # default == sub
