from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    student_id: str
    student_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: str
