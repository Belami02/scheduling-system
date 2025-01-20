from app.database.db import database
from app.models.availability import AvailabilityModel
from bson import ObjectId

async def add_availability(availability: AvailabilityModel):
    tutor = await database["tutors"].find_one({"tutor_id": availability.tutor_id})

    if not tutor:
        # Add tutor information if it doesn't exist
        tutor_data = {
            "tutor_id": availability.tutor_id,
            "tutor_name": availability.tutor_name
        }
        await database["tutors"].insert_one(tutor_data)

    # Add the new availability slot (avoid duplication)
    existing_availability = await database["availabilities"].find_one({
        "tutor_id": availability.tutor_id,
        "day_of_week": availability.day_of_week,
        "start_time": availability.start_time,
        "end_time": availability.end_time,
    })

    if existing_availability:
        raise ValueError("This availability slot already exists.")

    result = await database["availabilities"].insert_one(availability.dict())
    return str(result.inserted_id)

async def get_availability(tutor_id: str):
    availabilities = await database["availabilities"].find({"tutor_id": tutor_id}).to_list(100)
    for availability in availabilities:
        availability["_id"] = str(availability["_id"])
    return availabilities

async def delete_availability(availability_id: str):
    result = await database["availabilities"].delete_one({"_id": ObjectId(availability_id)})
    if result.deleted_count == 0:
        raise ValueError("Availability slot not found.")
    return True
