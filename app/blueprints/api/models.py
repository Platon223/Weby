from app.extensions.db import db
from sqlalchemy import Column, Text, Integer
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(Text, nullable=False)
    username = Column(Text, primary_key=True)
    password = Column(Text, nullable=False)
    email = Column(Text)
    job = Column(Text)

    def get_id(self):
        return self.username