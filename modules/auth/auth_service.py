from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.jwt_utils import create_access_token
from bson import ObjectId

# MOCKED OTP
MOCKED_OTP = "123456"

async def request_otp(phone: str, db: AsyncIOMotorDatabase):
    user = await db.users.find_one({"phone": phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Normally integrate 2Factor here, for now return mocked
    return MOCKED_OTP

async def verify_otp(phone: str, otp: str, db: AsyncIOMotorDatabase):
    if otp != MOCKED_OTP:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user = await db.users.find_one({"phone": phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_access_token({"user_id": str(user["_id"]), "phone": user["phone"], "role": user["role"]})
    return token

async def register_user(data: dict, db: AsyncIOMotorDatabase):
    existing = await db.users.find_one({"phone": data["phone"]})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    result = await db.users.insert_one(data)
    return str(result.inserted_id)

async def login_with_pin(phone: str, pin: str, db: AsyncIOMotorDatabase):
    user = await db.users.find_one({"phone": phone})
    if not user or user.get("pin") != pin:
        raise HTTPException(status_code=401, detail="Invalid phone or PIN")
    token = create_access_token({"user_id": str(user["_id"]), "phone": phone, "role": user["role"]})
    return token
