from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from config import MONGODB_URI, MONGO_DB_NAME

# Sync client for scripts/console
client = None
db = None

def connect_to_mongo_sync():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGO_DB_NAME]

def get_database():
    if db is None:
        raise Exception("Database not initialized. Call connect_to_mongo_sync() first.")
    return db

# ✅ For FastAPI app: attaches to app.state
async def connect_to_mongo(app: FastAPI):
    app.state.client = AsyncIOMotorClient(MONGODB_URI)
    app.state.database = app.state.client[MONGO_DB_NAME]
