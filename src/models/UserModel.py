from app import db


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return f"<Provider(id={self.id}, name={self.name})>"
