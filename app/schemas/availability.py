from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date
import pytz

class AvailabilityBase(BaseModel):
    tutor_id: str
    tutor_name: str
    day_of_week: str
    start_time: str  # Expect string format 'YYYY-MM-DDTHH:MM' or 'YYYY-MM-DDTHH:MM:SS'
    end_time: str
    is_recurring: bool
    recurrence_start: Optional[str] = None
    recurrence_end: Optional[str] = None
    time_zone: str

    @validator("time_zone")
    def validate_time_zone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError("Invalid time zone")
        return v

    @validator("start_time", "end_time", pre=True)
    def validate_time_format(cls, v):
        formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"]
        for fmt in formats:
            try:
                return datetime.strptime(v, fmt).isoformat()
            except ValueError:
                continue
        raise ValueError("Invalid datetime format, use YYYY-MM-DDTHH:MM or YYYY-MM-DDTHH:MM:SS")

    @validator("recurrence_start", "recurrence_end", pre=True)
    def validate_date_format(cls, v):
        if v:
            try:
                return datetime.strptime(v, "%Y-%m-%d").date().isoformat()
            except ValueError:
                raise ValueError("Invalid date format, use YYYY-MM-DD")
        return v

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityResponse(BaseModel):
    id: str
    tutor_id: str
    tutor_name: str
    day_of_week: str
    start_time: str
    end_time: str
    is_recurring: bool
    recurrence_start: Optional[str] = None
    recurrence_end: Optional[str] = None
    time_zone: str
