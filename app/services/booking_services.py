from app.database.db import database
from app.models.booking import BookingModel
from bson import ObjectId

async def add_booking(booking: BookingModel):
    # Check if the tutor exists
    tutor = await database["tutors"].find_one({"tutor_id": booking.tutor_id})
    if not tutor:
        raise ValueError("Tutor does not exist.")

    # Ensure no duplicate bookings (tutor-student-time uniqueness)
    existing_booking = await database["bookings"].find_one({
        "tutor_id": booking.tutor_id,
        "student_id": booking.student_id,
        "booking_date": booking.booking_date,
        "start_time": booking.start_time,
        "end_time": booking.end_time
    })

    if existing_booking:
        raise ValueError("This booking already exists.")

    booking_data = booking.dict()
    result = await database["bookings"].insert_one(booking_data)
    return str(result.inserted_id)

async def get_bookings_by_student(student_id: str):
    bookings = await database["bookings"].find({"student_id": student_id}).to_list(100)
    for booking in bookings:
        booking["_id"] = str(booking["_id"])
    return bookings

async def cancel_booking(booking_id: str):
    result = await database["bookings"].delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 0:
        raise ValueError("Booking not found.")
    return True
