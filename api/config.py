import datetime
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    basedir = Path.cwd()
    DATABASE = "flaskr.db"
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
