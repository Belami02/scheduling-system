from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db


# Course Model
class CourseModel:
    def __init__(self, course_id: str, course_name: str):
        self.course_id = course_id
        self.course_name = course_name

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            course_id=data["course_id"],
            course_name=data["course_name"]
        )