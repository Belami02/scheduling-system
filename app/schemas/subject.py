from pydantic import BaseModel
from typing import Optional

class SubjectBase(BaseModel):
    subject_id: str
    subject_name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: str
