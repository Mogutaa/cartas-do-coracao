from datetime import datetime
import uuid
from pymongo import MongoClient
from config.settings import settings

class Group:
    def __init__(self, name: str, user_id: str, _id: str = None):
        self.id = _id or str(uuid.uuid4())
        self.name = name
        self.user_id = user_id
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            '_id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            user_id=data['user_id'],
            _id=data['_id']
        )