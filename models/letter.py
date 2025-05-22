from datetime import datetime
import uuid
from config.settings import settings
from pymongo import MongoClient
import uuid

client = MongoClient(settings.MONGO_URI)
db = client.cartas_coracao


class Letter:
    def __init__(self, content: str, group_id: str, user_id: str, sentiment: str, _id: str = None):
        self.created_at = datetime.now()
        self.id = _id or str(uuid.uuid4())
        self.content = content
        self.group_id = group_id
        self.user_id = user_id
        self.sentiment = sentiment
        self.responses = []  # Lista de respostas
        self.share_id = str(uuid.uuid4())  # ID único para compartilhamento
        self.is_favorite = False
        if not hasattr(self, 'share_id') or not self.share_id:
            self.share_id = str(uuid.uuid4())

    def to_dict(self):
        return {
            '_id': self.id,
            'content': self.content,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'sentiment': self.sentiment,
            'created_at': self.created_at,
            'responses': self.responses,
            'share_id': self.share_id,
            'is_favorite': self.is_favorite
        }

    def add_response(self, letter_id: str, response: str):
        db.letters.update_one(
            {"_id": letter_id},
            {"$push": {"responses": {
                "content": response,
                "created_at": datetime.now()  
            }}}
        )

    @classmethod
    def from_dict(cls, data: dict):
        letter = cls(
            content=data['content'],
            group_id=data['group_id'],
            user_id=data['user_id'],
            sentiment=data['sentiment'],
            _id=data['_id']
        )
        letter.responses = data.get('responses', [])
        letter.is_favorite = data.get('is_favorite', False)
        return letter