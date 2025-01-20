from app.database.db import database
from app.models.booking import BookingModel
from bson import ObjectId

async def add_booking(data):
    booking = BookingModel(**data.dict())
    
    # Check for conflicts before inserting
    existing_booking = await database["bookings"].find_one({
        "tutor_id": booking.tutor_id,
        "booking_date": booking.booking_date,
        "start_time": booking.start_time,
        "end_time": booking.end_time
    })
    
    if existing_booking:
        raise ValueError("Slot already booked.")
    
    result = await database["bookings"].insert_one(booking.to_dict())
    return str(result.inserted_id)

async def get_bookings_by_student(student_id: str):
    bookings = await database["bookings"].find({"student_id": student_id}).to_list(100)
    return [BookingModel.from_dict(booking).to_dict() for booking in bookings]

async def cancel_booking(booking_id: str):
    result = await database["bookings"].delete_one({"_id": ObjectId(booking_id)})
    return result.deleted_count
