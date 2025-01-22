"""
This module contains the models for the application.
"""

from datetime import time, date
from pydantic import BaseModel
from typing import List, Optional


"""
Booking model
"""
class BookingModel(BaseModel):
    student_id: str
    tutor_id: str
    tutor_name: str
    booking_date: date
    start_time: time
    end_time: time
    subject: str
    time_zone: str

    class Config:
        from_attributes = True

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "tutor_id": self.tutor_id,
            "tutor_name": self.tutor_name,
            "booking_date": self.booking_date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
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


"""
Course model
"""
class CourseModel(BaseModel):
    course_id: str
    course_name: str

    class Config:
        from_attributes = True

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


"""
Role Model
"""
class RoleModel(BaseModel):
    role_name: str

    class Config:
        from_attributes = True

    def to_dict(self):
        return {
            "role_name": self.role_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(role_name=data["role_name"])


"""
Availability Slot Model
"""
class AvailabilitySlot(BaseModel):
    recurring: bool
    time_start: time
    time_end: time
    recurrence_start: Optional[date] = None
    recurrence_end: Optional[date] = None

    def to_dict(self):
        return {
            "recurring": self.recurring,
            "time_start": self.time_start.isoformat(),
            "time_end": self.time_end.isoformat(),
            "recurrence_start": self.recurrence_start.isoformat() if self.recurrence_start else None,
            "recurrence_end": self.recurrence_end.isoformat() if self.recurrence_end else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            recurring=data["recurring"],
            time_start=time.fromisoformat(data["time_start"]),
            time_end=time.fromisoformat(data["time_end"]),
            recurrence_start=date.fromisoformat(data["recurrence_start"]) if data["recurrence_start"] else None,
            recurrence_end=date.fromisoformat(data["recurrence_end"]) if data["recurrence_end"] else None
        )


"""
Tutor Availability Model
"""
class TutorAvailabilityModel(BaseModel):
    course_id: str
    user_id: str
    availability: List[AvailabilitySlot]

    class Config:
        from_attributes = True

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "user_id": self.user_id,
            "availability": [slot.to_dict() for slot in self.availability]
        }

    @classmethod
    def from_dict(cls, data):
        availability = [AvailabilitySlot.from_dict(slot) for slot in data["availability"]]
        return cls(
            course_id=data["course_id"],
            user_id=data["user_id"],
            availability=availability
        )


"""
User Model
"""
class UserModel(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    timezone: str

    class Config:
        from_attributes = True

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
