from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from fastapi import FastAPI, Request
from config import MONGODB_URI, MONGO_DB_NAME

# Used in old-style global imports
client = None
db: Database = None

def connect_to_mongo_sync():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGO_DB_NAME]

def get_database() -> Database:
    if db is None:
        raise Exception("Database not initialized. Call connect_to_mongo_sync() first.")
    return db

# ✅ For FastAPI startup
async def connect_to_mongo(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGO_DB_NAME]  # 🟢 Now sets global `db` too for old imports
    app.state.client = client
    app.state.database = db

# ✅ For FastAPI routes (preferred)
def get_db(request: Request):
    db = request.app.state.database
    if not db:
        raise RuntimeError("Database not initialized. Check MongoDB connection.")
    return db
