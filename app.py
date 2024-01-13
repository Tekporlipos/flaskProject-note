from flask import Flask
from flask_jwt_extended import JWTManager

from instance.dbconfig import DbConfig
from migration.Base import db
from dotenv import load_dotenv
from instance.logger import setup_logging

load_dotenv()
app = Flask(__name__)
app.config.from_object(DbConfig)
db.init_app(app)
setup_logging(app)
jwt = JWTManager(app)
import routes.api
import routes.web


with app.app_context():
    import src.models.UserModel
    import src.models.RatesModel
    import src.models.NoteModel
    db.create_all()

if __name__ == '__main__':
    app.run()
