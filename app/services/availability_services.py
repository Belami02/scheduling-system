from app.database.db import database
from app.models.availability import AvailabilityModel
from bson import ObjectId

async def add_availability(data):
    availability = AvailabilityModel(**data.dict())
    result = await database["availability"].insert_one(availability.to_dict())
    return str(result.inserted_id)

async def get_availability(tutor_id: str):
    availability_list = await database["availability"].find({"tutor_id": tutor_id}).to_list(100)
    return [AvailabilityModel.from_dict(avail).to_dict() for avail in availability_list]

async def delete_availability(availability_id: str):
    result = await database["availability"].delete_one({"_id": ObjectId(availability_id)})
    return result.deleted_count
