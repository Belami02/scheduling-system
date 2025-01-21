from fastapi import APIRouter, HTTPException
from app.schemas.booking import BookingCreate, BookingResponse
from app.database.db import database
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/booking/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate):
    try:
        # Ensure student and subject exist
        student = await database["students"].find_one({"student_id": booking.student_id})
        subject = await database["subjects"].find_one({"subject_id": booking.subject})

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Convert booking_date, start_time, and end_time to string format
        booking_data = booking.dict()
        booking_data["booking_date"] = booking.booking_date.strftime("%Y-%m-%d")
        booking_data["start_time"] = booking.start_time.strftime("%Y-%m-%dT%H:%M:%S")
        booking_data["end_time"] = booking.end_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Check for overlapping bookings for the same tutor on the same date
        existing_booking = await database["bookings"].find_one({
            "tutor_id": booking.tutor_id,
            "booking_date": booking_data["booking_date"],
            "$or": [
                {
                    "start_time": {"$lt": booking_data["end_time"]},
                    "end_time": {"$gt": booking_data["start_time"]}
                }
            ]
        })

        if existing_booking:
            raise HTTPException(status_code=400, detail="This slot is already booked.")

        result = await database["bookings"].insert_one(booking_data)
        booking_data["id"] = str(result.inserted_id)
        del booking_data["_id"]

        return booking_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/booking/{student_id}", response_model=List[BookingResponse])
async def get_student_bookings(student_id: str):
    bookings = await database["bookings"].find({"student_id": student_id}).to_list(100)
    
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this student.")
    
    for booking in bookings:
        booking["id"] = str(booking.pop("_id"))
        booking["booking_date"] = booking["booking_date"].strftime("%Y-%m-%d")

    return bookings


@router.delete("/booking/{booking_id}")
async def cancel_booking(booking_id: str):
    try:
        result = await database["bookings"].delete_one({"_id": ObjectId(booking_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Booking not found.")

        return {"message": "Booking canceled successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bookings/")
async def fetch_all_bookings():
    try:
        bookings_cursor = database["bookings"].find()
        bookings = []
        async for booking in bookings_cursor:
            booking["id"] = str(booking.pop("_id"))  # Convert ObjectId to string
            bookings.append(booking)

        if not bookings:
            raise HTTPException(status_code=404, detail="No bookings found")
        
        return bookings

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
