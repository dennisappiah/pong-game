import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = Path.cwd()
    DATABASE = "flaskr.db"
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
