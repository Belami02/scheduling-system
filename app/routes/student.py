from fastapi import APIRouter, HTTPException
from app.schemas.student import StudentCreate, StudentResponse
from app.database.db import database
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate):
    existing_student = await database["students"].find_one({"student_id": student.student_id})
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists.")
    
    student_data = student.dict()
    result = await database["students"].insert_one(student_data)
    student_data["id"] = str(result.inserted_id)
    return student_data

@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    student = await database["students"].find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student["_id"])
    del student["_id"]
    return student

@router.get("/students/", response_model=List[StudentResponse])
async def list_students():
    students_cursor = database["students"].find()
    students = []
    async for student in students_cursor:
        student["id"] = str(student["_id"])
        del student["_id"]
        students.append(student)
    
    return students
