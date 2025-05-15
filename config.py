import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")

if not MONGODB_URI:
    raise ValueError("⚠️ MONGODB_URI not found in environment variables.")
if not MONGO_DB_NAME:
    raise ValueError("⚠️ MONGO_DB_NAME not found in environment variables.")
if not JWT_SECRET:
    raise ValueError("⚠️ JWT_SECRET not found in environment variables.")
