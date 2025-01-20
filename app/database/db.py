from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "scheduling-db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# Collections for better code readability
tutors_collection = database["tutors"]
availabilities_collection = database["availabilities"]
bookings_collection = database["bookings"]
