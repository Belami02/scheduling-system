from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db

# Tutor Availability Model
class TutorAvailabilityModel:
    def __init__(self, course_id: str, user_id: str):
        self.course_id = course_id
        self.user_id = user_id
        self.availability = []  # List of availability slots

    def add_availability_slot(self, recurring: bool, time_start: time, time_end: time, recurrence_start: date = None, recurrence_end: date = None):
        slot = {
            "recurring": recurring,
            "time_start": time_start.strftime("%H:%M"),
            "time_end": time_end.strftime("%H:%M"),
            "recurrence_start": recurrence_start.strftime("%Y-%m-%d") if recurrence_start else None,
            "recurrence_end": recurrence_end.strftime("%Y-%m-%d") if recurrence_end else None
        }
        self.availability.append(slot)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "user_id": self.user_id,
            "availability": self.availability
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            course_id=data["course_id"],
            user_id=data["user_id"]
        )
        instance.availability = data["availability"]
        return instance