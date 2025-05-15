import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
TWO_FACTOR_API_KEY = "acd01d56-2fbd-11f0-8b17-0200cd936042"

if not MONGODB_URI:
    raise ValueError("⚠️ MONGODB_URI not found in environment variables.")
if not MONGO_DB_NAME:
    raise ValueError("⚠️ MONGO_DB_NAME not found in environment variables.")
if not JWT_SECRET:
    raise ValueError("⚠️ JWT_SECRET not found in environment variables.")
