"""
This is the User model that will be used in the application.
"""

from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db

# user Model
class UserModel:
    def __init__(self, user_id: str, name: str, email: str, role: str, timezone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.timezone = timezone

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "timezone": self.timezone
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            role=data["role"],
            timezone=data["timezone"]
        )