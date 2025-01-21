from fastapi import APIRouter, HTTPException
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.database.db import database
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/subjects/", response_model=SubjectResponse)
async def create_subject(subject: SubjectCreate):
    existing_subject = await database["subjects"].find_one({"subject_id": subject.subject_id})
    if existing_subject:
        raise HTTPException(status_code=400, detail="Subject ID already exists.")
    
    subject_data = subject.dict()
    result = await database["subjects"].insert_one(subject_data)
    subject_data["id"] = str(result.inserted_id)
    return subject_data

@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
async def get_subject(subject_id: str):
    subject = await database["subjects"].find_one({"subject_id": subject_id})
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject["id"] = str(subject["_id"])
    del subject["_id"]
    return subject

@router.get("/subjects/", response_model=List[SubjectResponse])
async def list_subjects():
    subjects_cursor = database["subjects"].find()
    subjects = []
    async for subject in subjects_cursor:
        subject["id"] = str(subject["_id"])
        del subject["_id"]
        subjects.append(subject)
    
    return subjects
