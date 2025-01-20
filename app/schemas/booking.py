from pydantic import BaseModel, validator
from datetime import date, time
from typing import Optional
import pytz
from app.database.db import database 

class BookingCreate(BaseModel):
    student_id: str
    tutor_id: str
    tutor_name: str
    booking_date: date
    start_time: time
    end_time: time
    subject: str
    time_zone: str
    
    @validator("time_zone")
    def validate_time_zone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError("Invalid time zone")
        return v

class BookingResponse(BookingCreate):
    id: str
