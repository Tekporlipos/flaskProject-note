from flask import Flask

from instance.dbconfig import DbConfig
from migration.Base import db
from dotenv import load_dotenv
from instance.logger import setup_logging

load_dotenv()
app = Flask(__name__)
app.config.from_object(DbConfig)
db.init_app(app)
setup_logging(app)
import routes.api


with app.app_context():
    import src.models.NoteModel
    db.create_all()

if __name__ == '__main__':
    app.run()
