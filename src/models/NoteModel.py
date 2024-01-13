import uuid

from sqlalchemy.orm import relationship

from app import db


class Notes(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False, unique=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return (f"<Notes(id={self.id}, title={self.title}, body={self.body}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")
