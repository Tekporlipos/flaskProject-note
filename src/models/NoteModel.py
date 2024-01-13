import uuid

from sqlalchemy.orm import relationship

from app import db


class Notes(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='notes')
    title = db.Column(db.String(50), unique=True, nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return (f"<Notes(id={self.id}, user_id={self.user_id}, user={self.user}, title={self.title}, body={self.body},"
                f"created_at={self.created_at}, updated_at={self.updated_at})>")
