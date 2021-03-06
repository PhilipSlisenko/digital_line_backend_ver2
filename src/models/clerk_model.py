from datetime import datetime

from app import db, ma
from models.helpers import hash_password, verify_password_hash


class ClerkModel(db.Model):
    __tablename__ = "clerks"

    username = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    lines = db.relationship('LineModel', secondary="clerks_lines_link")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created_at = datetime.utcnow()

    @classmethod
    def check_if_user_exists(cls, username: str) -> bool:
        user = cls.query.filter_by(username=username).first()
        return True if user else False

    @classmethod
    def register_new_user(cls, username: str, password: str) -> "ClerkModel":
        user = cls(username=username, password=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        user = cls.query.filter_by(username=username).first()
        return verify_password_hash(password, user.password)

    @classmethod
    def get_by_username(cls, username: str) -> 'ClerkModel':
        return cls.query.filter_by(username=username).first()

    def my_lines(self):
        return self.lines
