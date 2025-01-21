from pydantic import BaseModel, validator
from datetime import datetime, date
import pytz

class BookingBase(BaseModel):
    student_id: str
    tutor_id: str
    booking_date: date  # Store booking_date as date type
    start_time: datetime  # Expect 'YYYY-MM-DDTHH:MM:SS' format
    end_time: datetime
    subject: str
    time_zone: str

    @validator("time_zone")
    def validate_time_zone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError("Invalid time zone")
        return v

    @validator("start_time", "end_time", pre=True)
    def validate_time_format(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError("Invalid datetime format, use YYYY-MM-DDTHH:MM:SS")
        return v

    @validator("booking_date", pre=True)
    def validate_booking_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format, use YYYY-MM-DD")
        return v

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: str

    @validator("booking_date", pre=True, always=True)
    def format_booking_date(cls, v):
        if isinstance(v, date):  # If it's already a date object, format it
            return v.strftime("%Y-%m-%d")
        return v  # If it's a string, return as is
