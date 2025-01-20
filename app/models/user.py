from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr

class TutorCreate(UserBase):
    specialization: str

class TutorResponse(TutorCreate):
    id: str

class StudentCreate(UserBase):
    course: Optional[str] = None

class StudentResponse(StudentCreate):
    id: str
