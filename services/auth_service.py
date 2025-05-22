from models.user import User
from utils.security import hash_password, verify_password
from config.settings import settings
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)
db = client.cartas_coracao

class AuthService:
    @staticmethod
    def register_user(username: str, password: str) -> User:
        if db.users.find_one({"username": username}):
            raise ValueError("Usuário já existe")
        
        hashed = hash_password(password)
        user_data = User(username, hashed).to_dict()
        result = db.users.insert_one(user_data)
        return User.from_dict({**user_data, '_id': result.inserted_id})

    @staticmethod
    def authenticate(username: str, password: str) -> User:
        user_data = db.users.find_one({"username": username})
        if not user_data:
            raise ValueError("Usuário não encontrado")
        
        if verify_password(password, user_data['password']):
            return User.from_dict(user_data)
        raise ValueError("Credenciais inválidas")