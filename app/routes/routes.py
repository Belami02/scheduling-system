"""
This module contains the FastAPI routes for the application.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime, date
from app.schemas.models import BookingModel, CourseModel, RoleModel, TutorAvailabilityModel, UserModel
from app.database.db import database as db
from datetime import datetime, date, time

router = APIRouter()

# converting ObjectId to string
def objectid_to_str(obj):
    return str(obj) if obj else None

# serializing datetime fields
def serialize_datetime_fields(data: dict):
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.isoformat()  # 'YYYY-MM-DD'
        elif isinstance(value, time):
            data[key] = value.strftime("%H:%M:%S")  # 'HH:MM:SS'
        elif isinstance(value, list):  
            data[key] = [serialize_datetime_fields(item) if isinstance(item, dict) else item for item in value]
    return data

# converting date to datetime
def convert_date_to_datetime(date_obj):
    if isinstance(date_obj, date):
        return datetime.combine(date_obj, datetime.min.time())
    return date_obj

# checking for duplicates
async def is_duplicate(collection, query):
    return await collection.find_one(query) is not None

"""
The following routes are defined:
- /bookings
- /bookings/{booking_id}
"""
@router.post("/bookings", response_model=BookingModel)
async def create_booking(booking: BookingModel):
    booking_dict = booking.dict()
    booking_dict = serialize_datetime_fields(booking_dict)
    # Check for duplicate booking
    if await is_duplicate(db.booking, 
                          {"booking_date": booking_dict["booking_date"], 
                           "tutor_id": booking.tutor_id, "start_time": 
                           booking_dict["start_time"], 
                           "end_time": booking_dict["end_time"]}):
        raise HTTPException(status_code=400, detail="Booking already exists for this user on the same date.")

    result = await db.booking.insert_one(booking_dict)
    booking_dict["_id"] = result.inserted_id
    return BookingModel.from_dict(booking_dict)

@router.get("/bookings", response_model=List[BookingModel])
async def get_all_bookings():
    bookings_cursor = db.booking.find()
    bookings_list = await bookings_cursor.to_list(length=None)  # Convert the cursor to a list
    return [BookingModel.from_dict(booking) for booking in bookings_list]

@router.get("/bookings/{booking_id}", response_model=BookingModel)
async def get_booking(booking_id: str):
    booking = await db.booking.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingModel.from_dict(booking)

@router.delete("/bookings/{booking_id}", status_code=204)
async def delete_booking(booking_id: str):
    result = await db.booking.delete_one({"_id": ObjectId(booking_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")


"""
The following routes are defined:
- /courses
- /courses/{course_id}
"""
@router.post("/courses", response_model=CourseModel)
async def create_course(course: CourseModel):
    # Check for duplicate course
    if await is_duplicate(db.course, {"course_id": course.course_id}):
        raise HTTPException(status_code=400, detail="Course with this ID already exists.")
    
    course_dict = course.dict()
    course_dict["start_date"] = convert_date_to_datetime(course_dict.get("start_date"))
    result = await db.course.insert_one(course_dict)
    course_dict["_id"] = result.inserted_id
    return CourseModel.from_dict(course_dict)

@router.get("/courses", response_model=List[CourseModel])
async def get_all_courses():
    courses_cursor = db.course.find()
    courses_list = await courses_cursor.to_list(length=None)
    return [CourseModel.from_dict(course) for course in courses_list]

@router.get("/courses/{course_id}", response_model=CourseModel)
async def get_course(course_id: str):
    course = await db.course.find_one({"course_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseModel.from_dict(course)

@router.delete("/courses/{course_id}", status_code=204)
async def delete_course(course_id: str):
    result = await db.course.delete_one({"course_id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")


"""
The following routes are defined:
- /roles
- /roles/{role_name}
"""
@router.post("/roles", response_model=RoleModel)
async def create_role(role: RoleModel):
    # check for duplicate role
    if await is_duplicate(db.role, {"role_name": role.role_name}):
        raise HTTPException(status_code=400, detail="Role with this name already exists.")
    
    result = await db.role.insert_one(role.dict())
    role_dict = role.dict()
    role_dict["_id"] = result.inserted_id
    return RoleModel.from_dict(role_dict)

@router.get("/roles", response_model=List[RoleModel])
async def get_all_roles():
    roles_cursor = db.role.find()
    roles_list = await roles_cursor.to_list(length=None)
    return [RoleModel.from_dict(role) for role in roles_list]

@router.get("/roles/{role_name}", response_model=RoleModel)
async def get_role(role_name: str):
    role = await db.role.find_one({"role_name": role_name})
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return RoleModel.from_dict(role)

@router.delete("/roles/{role_name}", status_code=204)
async def delete_role(role_name: str):
    result = await db.role.delete_one({"role_name": role_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Role not found")



"""
The following routes are defined:
- /tutor_availabilities
- /tutor_availabilities/{user_id}
"""
@router.post("/tutor_availabilities", response_model=TutorAvailabilityModel)
async def create_tutor_availability(tutor_availability: TutorAvailabilityModel):
    tutor_availability_dict = tutor_availability.dict()
    tutor_availability_dict = serialize_datetime_fields(tutor_availability_dict)
    
    # Check for duplicate availability
    if await is_duplicate(db.tutor_availability, {"user_id": tutor_availability.user_id}):
        raise HTTPException(status_code=400, detail="Tutor availability already exists for this user.")
    
    result = await db.tutor_availability.insert_one(tutor_availability_dict)
    tutor_availability_dict["_id"] = result.inserted_id
    return TutorAvailabilityModel.from_dict(tutor_availability_dict)


@router.get("/tutor_availabilities", response_model=List[TutorAvailabilityModel])
async def get_all_tutor_availabilities():
    tutor_availabilities_cursor = db.tutor_availability.find()
    tutor_availabilities_list = await tutor_availabilities_cursor.to_list(length=None)
    return [TutorAvailabilityModel.from_dict(tutor_availability) for tutor_availability in tutor_availabilities_list]

@router.get("/tutor_availabilities/{user_id}", response_model=TutorAvailabilityModel)
async def get_tutor_availability(user_id: str):
    tutor_availability = await db.tutor_availability.find_one({"user_id": user_id})
    if not tutor_availability:
        raise HTTPException(status_code=404, detail="Tutor availability not found")
    return TutorAvailabilityModel.from_dict(tutor_availability)

@router.delete("/tutor_availabilities/{user_id}", status_code=204)
async def delete_tutor_availability(user_id: str):
    result = await db.tutor_availability.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tutor availability not found")



"""
The following routes are defined:
- /users
- /users/{user_id}
"""
@router.post("/users", response_model=UserModel)
async def create_user(user: UserModel):
    user_dict = user.dict()
    
    if user_dict.get('date_joined'):
        user_dict['date_joined'] = convert_date_to_datetime(user_dict['date_joined'])
    
    # check for duplicate user
    if await is_duplicate(db.user, {"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail="User with this ID already exists.")
    
    result = await db.user.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return UserModel.from_dict(user_dict)

@router.get("/users", response_model=List[UserModel])
async def get_all_users():
    users_cursor = db.user.find()
    users_list = await users_cursor.to_list(length=None)
    return [UserModel.from_dict(user) for user in users_list]

@router.get("/users/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = await db.user.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserModel.from_dict(user)

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    result = await db.user.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
