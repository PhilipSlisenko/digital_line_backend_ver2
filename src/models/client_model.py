from datetime import datetime

from app import db
from models.helpers import hash_password, verify_password_hash


class ClientModel(db.Model):
    __tablename__ = "clients"

    username = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    lines = db.relationship('LineModel', secondary="clients_lines_link")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created_at = datetime.utcnow()

    def my_lines(self):
        return self.lines

    @classmethod
    def check_if_user_exists(cls, username: str) -> bool:
        user = cls.query.filter_by(username=username).first()
        return True if user else False

    @classmethod
    def register_new_user(cls, username: str, password: str) -> "ClientModel":
        user = cls(username=username, password=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        user = cls.query.filter_by(username=username).first()
        return verify_password_hash(password, user.password)

    @classmethod
    def get_by_username(cls, username: str) -> 'ClientModel':
        return cls.query.filter_by(username=username).first()
