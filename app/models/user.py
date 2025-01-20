from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "student"  # Default role is student
