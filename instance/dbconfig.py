from instance.config import Config


class DbConfig:
    SQLALCHEMY_DATABASE_URI = Config.db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
