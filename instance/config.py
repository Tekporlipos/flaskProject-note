import os


class Config:
    db_url = os.environ.get('DATABASE_URI')
    flask_env = os.environ.get('FLASK_ENV')
