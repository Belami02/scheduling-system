"""
This module contains the Booking Model.
"""
from datetime import time, date
from pymongo import MongoClient

client = MongoClient()
db = client.scheduling_db

# Booking Model
class BookingModel:
    def __init__(self, student_id: str, tutor_id: str, tutor_name: str, booking_date: date,
                 start_time: time, end_time: time, subject: str, time_zone: str):
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.tutor_name = tutor_name
        self.booking_date = booking_date.strftime("%Y-%m-%d")
        self.start_time = start_time.strftime("%H:%M")
        self.end_time = end_time.strftime("%H:%M")
        self.subject = subject
        self.time_zone = time_zone

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "tutor_id": self.tutor_id,
            "tutor_name": self.tutor_name,
            "booking_date": self.booking_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "subject": self.subject,
            "time_zone": self.time_zone
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            tutor_id=data["tutor_id"],
            tutor_name=data["tutor_name"],
            booking_date=date.fromisoformat(data["booking_date"]),
            start_time=time.fromisoformat(data["start_time"]),
            end_time=time.fromisoformat(data["end_time"]),
            subject=data["subject"],
            time_zone=data["time_zone"]
        )
