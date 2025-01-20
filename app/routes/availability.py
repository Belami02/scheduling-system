from fastapi import APIRouter, HTTPException
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.services.availability_services import add_availability, get_availability, delete_availability
from app.database.db import database
from typing import List
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/availability/", response_model=AvailabilityResponse)
async def create_availability(availability: AvailabilityCreate):
    tutor = await database["tutors"].find_one({"tutor_id": availability.tutor_id})

    if not tutor:
        tutor_data = {
            "tutor_id": availability.tutor_id,
            "tutor_name": availability.tutor_name
        }
        await database["tutors"].insert_one(tutor_data)

    # Convert start_time and end_time from string to datetime
    start_time = datetime.strptime(availability.start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(availability.end_time, "%Y-%m-%dT%H:%M:%S")

    # Check for existing availability to prevent duplicates
    existing_availability = await database["availabilities"].find_one({
        "tutor_id": availability.tutor_id,
        "day_of_week": availability.day_of_week,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    })

    if existing_availability:
        raise HTTPException(status_code=400, detail="Duplicate availability exists")

    availability_data = availability.dict()
    availability_data["start_time"] = start_time.isoformat()
    availability_data["end_time"] = end_time.isoformat()

    # Convert recurrence_start and recurrence_end safely to date objects
    if availability.recurrence_start:
        recurrence_start = datetime.strptime(availability.recurrence_start, "%Y-%m-%d").date()
        availability_data["recurrence_start"] = recurrence_start.isoformat()

    if availability.recurrence_end:
        recurrence_end = datetime.strptime(availability.recurrence_end, "%Y-%m-%d").date()
        availability_data["recurrence_end"] = recurrence_end.isoformat()

    result = await database["availabilities"].insert_one(availability_data)
    availability_data["id"] = str(result.inserted_id)
    del availability_data["_id"]

    return availability_data


@router.get("/availability/{tutor_id}", response_model=List[AvailabilityResponse])
async def get_tutor_availability(tutor_id: str):
    availabilities = await database["availabilities"].find({"tutor_id": tutor_id}).to_list(100)
    
    if not availabilities:
        raise HTTPException(status_code=404, detail="Tutor not found")

    # Convert MongoDB '_id' to 'id' and remove duplicates
    unique_availabilities = []
    seen_availability = set()

    for availability in availabilities:
        key = (
            availability["tutor_id"],
            availability["day_of_week"],
            availability["start_time"],
            availability["end_time"],
        )
        if key not in seen_availability:
            seen_availability.add(key)
            availability['id'] = str(availability.pop('_id'))
            unique_availabilities.append(availability)

    return unique_availabilities


@router.delete("/availability/{availability_id}")
async def delete_availability(availability_id: str):
    result = await database["availabilities"].delete_one({"_id": ObjectId(availability_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Availability slot not found.")
    
    return {"message": "Availability deleted successfully"}


@router.get("/tutors/")
async def fetch_all_tutors():
    try:
        tutors_cursor = database["tutors"].find()
        tutors = []
        async for tutor in tutors_cursor:
            tutor["_id"] = str(tutor["_id"])  # Convert ObjectId to string
            tutors.append(tutor)

        if not tutors:
            raise HTTPException(status_code=404, detail="No tutors found")
        
        return tutors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
