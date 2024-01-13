from app import db


class Trucks(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', backref=db.backref('trucks', lazy=True))

    def __repr__(self):
        return f"<Trucks(id={self.id}, provider_id={self.provider_id})>"
