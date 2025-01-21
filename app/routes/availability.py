from fastapi import APIRouter, HTTPException
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.services.availability_services import add_availability, get_availability, delete_availability
from app.database.db import database
from typing import List
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/availability/")
async def create_availability(availabilities: List[AvailabilityCreate]):
    tutor_id = availabilities[0].tutor_id
    tutor_name = availabilities[0].tutor_name

    # Check if the tutor already exists
    existing_tutor = await database["tutors"].find_one({"tutor_id": tutor_id})

    availability_list = []
    for availability in availabilities:
        start_time = datetime.strptime(availability.start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(availability.end_time, "%Y-%m-%dT%H:%M:%S")

        availability_data = {
            "day_of_week": availability.day_of_week,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "is_recurring": availability.is_recurring,
            "recurrence_start": availability.recurrence_start,
            "recurrence_end": availability.recurrence_end,
            "time_zone": availability.time_zone
        }
        availability_list.append(availability_data)

    if existing_tutor:
        # Update existing tutor's availabilities without duplication
        await database["tutors"].update_one(
            {"tutor_id": tutor_id},
            {"$addToSet": {"availabilities": {"$each": availability_list}}}
        )
    else:
        # Insert new tutor record
        tutor_data = {
            "tutor_id": tutor_id,
            "tutor_name": tutor_name,
            "availabilities": availability_list
        }
        await database["tutors"].insert_one(tutor_data)

    # Retrieve updated tutor data
    updated_tutor = await database["tutors"].find_one({"tutor_id": tutor_id}, {"_id": 0})

    return updated_tutor


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
