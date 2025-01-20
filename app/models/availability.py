from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db

class AvailabilityModel:
    def __init__(self, tutor_id: str, tutor_name: str, day_of_week: str,
                 start_time: time, end_time: time, is_recurring: bool,
                 recurrence_start: date = None, recurrence_end: date = None,
                 time_zone: str = "UTC"):
        self.tutor_id = tutor_id
        self.tutor_name = tutor_name
        self.day_of_week = day_of_week
        self.start_time = start_time.strftime("%H:%M")
        self.end_time = end_time.strftime("%H:%M")
        self.is_recurring = is_recurring
        self.recurrence_start = recurrence_start.strftime("%Y-%m-%d") if recurrence_start else None
        self.recurrence_end = recurrence_end.strftime("%Y-%m-%d") if recurrence_end else None
        self.time_zone = time_zone

    def to_dict(self):
        return {
            "tutor_id": self.tutor_id,
            "tutor_name": self.tutor_name,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_recurring": self.is_recurring,
            "recurrence_start": self.recurrence_start,
            "recurrence_end": self.recurrence_end,
            "time_zone": self.time_zone
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tutor_id=data["tutor_id"],
            tutor_name=data["tutor_name"],
            day_of_week=data["day_of_week"],
            start_time=time.fromisoformat(data["start_time"]),
            end_time=time.fromisoformat(data["end_time"]),
            is_recurring=data["is_recurring"],
            recurrence_start=date.fromisoformat(data["recurrence_start"]) if data.get("recurrence_start") else None,
            recurrence_end=date.fromisoformat(data["recurrence_end"]) if data.get("recurrence_end") else None,
            time_zone=data["time_zone"]
        )
