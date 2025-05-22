# services/group_service.py
from pymongo import MongoClient
from config.settings import settings
from models.group import Group
from typing import List

client = MongoClient(settings.MONGO_URI)
db = client.cartas_coracao

class GroupService:
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def create_group(self, name: str) -> Group:
        if not name:
            raise ValueError("O nome do grupo não pode ser vazio")
        
        existing = db.groups.find_one({
            "user_id": self.user_id,
            "name": name.lower().strip()
        })
        
        if existing:
            raise ValueError("Você já tem um grupo com este nome")
        
        group = Group(
            name=name.strip(),
            user_id=self.user_id
        )
        
        db.groups.insert_one(group.to_dict())
        return group
    
    def get_user_groups(self) -> List[Group]:
        groups = db.groups.find({"user_id": self.user_id})
        return [Group.from_dict(g) for g in groups]
    
    def update_group(self, group_id: str, new_name: str) -> Group:
        """Atualiza o nome de um grupo existente"""
        group = db.groups.find_one({
            "_id": group_id,
            "user_id": self.user_id
        })
        
        if not group:
            raise ValueError("Grupo não encontrado")
        
        updated = db.groups.update_one(
            {"_id": group_id},
            {"$set": {"name": new_name.strip()}}
        )
        
        if updated.modified_count == 0:
            raise ValueError("Falha ao atualizar o grupo")
        
        return Group(
            name=new_name,
            user_id=self.user_id,
            _id=group_id
        )
    
    def delete_group(self, group_id: str) -> bool:
        """Exclui um grupo e todas suas cartas relacionadas"""
        result = db.groups.delete_one({
            "_id": group_id,
            "user_id": self.user_id
        })
        
        if result.deleted_count == 0:
            raise ValueError("Grupo não encontrado ou não pertence ao usuário")
        
        # Exclui cartas associadas
        db.letters.delete_many({
            "group_id": group_id,
            "user_id": self.user_id
        })
        
        return True

    @staticmethod
    def from_dict(data: dict) -> Group:
        """Cria um objeto Group a partir de um dicionário"""
        return Group(
            name=data['name'],
            user_id=data['user_id'],
            _id=data['_id']
        )