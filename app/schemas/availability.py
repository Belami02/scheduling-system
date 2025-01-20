from pydantic import BaseModel, validator
from typing import Optional
from datetime import time, date
import pytz
from app.database.db import database 

class AvailabilityCreate(BaseModel):
    tutor_id: str
    tutor_name: str
    day_of_week: str
    start_time: time
    end_time: time
    is_recurring: bool
    recurrence_start: Optional[date] = None
    recurrence_end: Optional[date] = None
    time_zone: str

    @validator("time_zone")
    def validate_time_zone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError("Invalid time zone")
        return v

class AvailabilityResponse(AvailabilityCreate):
    id: str
