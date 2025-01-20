from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "scheduling-db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
