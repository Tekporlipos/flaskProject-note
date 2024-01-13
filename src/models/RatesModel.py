from app import db


class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(50))
    rate = db.Column(db.Integer, default=0)
    scope = db.Column(db.String(50))

    def __repr__(self):
        return f"<Rates(id={self.id}, product_id={self.product_id}, rate={self.rate}, scope={self.scope})>"
