from fastapi import APIRouter, HTTPException
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.services.availability_services import add_availability, get_availability, delete_availability
from app.database.db import database
from typing import List

router = APIRouter()

@router.post("/availability/", response_model=List[AvailabilityResponse])
async def create_multiple_availabilities(availabilities: List[AvailabilityCreate]):
    created_availabilities = []
    for availability in availabilities:
        availability_id = await add_availability(availability)
        created_availabilities.append({**availability.dict(), "id": availability_id})
    
    return created_availabilities

@router.get("/availability/{tutor_id}")
async def fetch_availability(tutor_id: str):
    availability = await get_availability(tutor_id)
    if not availability:
        raise HTTPException(status_code=404, detail="No availability found")
    return availability

@router.delete("/availability/{availability_id}")
async def remove_availability(availability_id: str):
    deleted_count = await delete_availability(availability_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}

@router.get("/tutors/")
async def fetch_all_tutors():
    try:
        tutors_cursor = database["availability"].find()
        tutors = []
        async for tutor in tutors_cursor:
            tutor["_id"] = str(tutor["_id"])  # Convert ObjectId to string
            tutors.append(tutor)

        if not tutors:
            raise HTTPException(status_code=404, detail="No tutors found")
        
        return tutors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
