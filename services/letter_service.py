from datetime import datetime
from models.letter import Letter
from config.settings import settings
from pymongo import MongoClient
import uuid


client = MongoClient(settings.MONGO_URI)
db = client.cartas_coracao

class LetterService:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def create_letter(self, content: str, group_id: str, sentiment: str) -> Letter:
        letter = Letter(
            content=content,
            group_id=group_id,
            user_id=self.user_id,
            sentiment=sentiment
        )
        db.letters.insert_one(letter.to_dict())
        return letter

    def get_letters_by_group(self, group_id: str):
        return [
            Letter.from_dict(letter)
            for letter in db.letters.find({
                "user_id": self.user_id,
                "group_id": group_id
            })
        ]
    
    def get_letter_by_share_id(self, share_id: str):
        return db.letters.find_one({"share_id": share_id})
    
    def add_response(self, letter_id: str, response: str):
        db.letters.update_one(
            {"_id": letter_id},
            {"$push": {"responses": {
                "content": response,
                "created_at": datetime.now()
            }}}
        )
    
    def get_share_link(self, letter_id: str) -> str:
        letter = db.letters.find_one({"_id": letter_id})
        if not letter:
            raise ValueError("Carta não encontrada")
        return f"{settings.BASE_URL}/?share_id={letter['share_id']}"

    def delete_letter(self, letter_id: str):
        # Verifica se a carta pertence ao usuário antes de deletar
        result = db.letters.delete_one({
            "_id": letter_id,
            "user_id": self.user_id
        })
        
        if result.deleted_count == 0:
            raise ValueError("Carta não encontrada ou você não tem permissão para excluí-la")
        
        return True