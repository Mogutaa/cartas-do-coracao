from datetime import datetime
from pymongo import MongoClient
from config.settings import settings

class User:
    def __init__(self, username: str, password: str = None, _id: str = None):
        self.id = _id
        self.username = username
        self.password = password
        self.created_at = datetime.now()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=str(data['_id']),
            username=data['username'],
            password=data['password'],
        )

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }