from app.extensions.db import db
from sqlalchemy import Column, Text, Integer, DateTime, func
from flask_login import UserMixin

class Message(db.Model):
    __tablename__ = 'messages'

    id = Column(Text, primary_key=True)
    sender = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)
    user_name = Column(Text, nullable=False)
    chat_id = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'chat_id': self.chat_id,
            'content': self.content,
            'timestamp': self.timestamp
        }

class Chat(db.Model):
    __tablename__ = 'chats'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)
    user_name = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'user_name': self.user_name
        }



