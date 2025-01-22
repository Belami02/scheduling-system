"""
This file is used to connect to the MongoDB database.
"""

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "scheduling-db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# tables in the database
users_collection = database["users"]
tutors_availabilities_collection = database["tutors"]
bookings_collection = database["bookings"]
roles_collection = database["roles"]
courses_collection = database["courses"]
