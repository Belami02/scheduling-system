from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db

class RoleModel:
    def __init__(self, role_name: str):
        self.role_name = role_name

    def to_dict(self):
        return {
            "role_name": self.role_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(role_name=data["role_name"])