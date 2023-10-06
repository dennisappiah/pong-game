import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = Path.cwd()
    DATABASE = "flaskr.db"
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=20)
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    basedir_ = Path.cwd()
    DATABASE_ = "test.db"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(basedir_).joinpath(DATABASE_)}"
    JWT_SECRET_KEY = "foobarbaz"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=1)


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
