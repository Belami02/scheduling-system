from fastapi import APIRouter, HTTPException
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_services import add_booking, get_bookings_by_student, cancel_booking
from app.database.db import database

router = APIRouter()

@router.post("/booking/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate):
    try:
        booking_id = await add_booking(booking)
        return {**booking.dict(), "id": booking_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/booking/{student_id}")
async def fetch_bookings(student_id: str):
    bookings = await get_bookings_by_student(student_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

@router.delete("/booking/{booking_id}")
async def remove_booking(booking_id: str):
    deleted_count = await cancel_booking(booking_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking cancelled successfully"}

@router.get("/bookings/")
async def fetch_all_bookings():
    try:
        bookings_cursor = database["bookings"].find()
        bookings = []
        async for booking in bookings_cursor:
            booking["_id"] = str(booking["_id"])  # Convert ObjectId to string
            bookings.append(booking)

        if not bookings:
            raise HTTPException(status_code=404, detail="No bookings found")
        
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))