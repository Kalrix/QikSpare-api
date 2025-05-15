from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI, MONGO_DB_NAME

client = None
db = None

def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGO_DB_NAME]

def get_database():
    if db is None:
        raise Exception("Database not initialized. Call connect_to_mongo() first.")
    return db
