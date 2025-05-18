from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from utils.jwt_utils import create_access_token
from datetime import datetime
import httpx
from config import TWO_FACTOR_API_KEY

TWO_FACTOR_URL = "https://2factor.in/API/V1"
OTP_TEMPLATE_NAME = "QIKSPARE"  # Ensure it's approved

# ---------------------------
# Send OTP using 2Factor API
# ---------------------------
async def request_otp(phone: str, db: AsyncIOMotorDatabase):
    url = f"{TWO_FACTOR_URL}/{TWO_FACTOR_API_KEY}/SMS/{phone}/AUTOGEN3/{OTP_TEMPLATE_NAME}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            data = response.json()
            if data["Status"] != "Success":
                raise HTTPException(status_code=400, detail="Failed to send OTP")
            return {"session_id": data["Details"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OTP request failed: {str(e)}")


# -----------------------------
# Verify OTP + Auto-register
# -----------------------------
async def verify_otp(phone: str, otp: str, session_id: str, role: str, db: AsyncIOMotorDatabase):
    url = f"{TWO_FACTOR_URL}/{TWO_FACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            data = response.json()
            if data["Status"] != "Success":
                raise HTTPException(status_code=400, detail="Invalid OTP")

            user = await db.users.find_one({"phone": phone})
            if not user:
                # Auto-create user with provided role (garage or vendor)
                new_user = {
                    "phone": phone,
                    "full_name": "New User",
                    "role": role,
                    "pin": None,
                    "referral_count": 0,
                    "referral_users": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
                result = await db.users.insert_one(new_user)
                user = await db.users.find_one({"_id": result.inserted_id})

            token = create_access_token({
                "user_id": str(user["_id"]),
                "phone": user["phone"],
                "role": user["role"]
            })
            return {"token": token}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OTP verification failed: {str(e)}")


# ------------------------
# Register New User (Manual Flow)
# ------------------------
async def register_user(data: dict, db: AsyncIOMotorDatabase):
    existing = await db.users.find_one({"phone": data["phone"]})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    result = await db.users.insert_one(data)
    return {"user_id": str(result.inserted_id)}


# -------------------------
# Login with 4-digit PIN
# -------------------------
async def login_with_pin(phone: str, pin: str, db: AsyncIOMotorDatabase):
    user = await db.users.find_one({"phone": phone})
    if not user or user.get("pin") != pin:
        raise HTTPException(status_code=401, detail="Invalid phone or PIN")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "phone": user["phone"],
        "role": user["role"]
    })
    return {"token": token}


# ✅ NEW FUNCTION: Update PIN for existing user
async def update_user_pin(phone: str, pin: str, db: AsyncIOMotorDatabase):
    user = await db.users.find_one({"phone": phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"phone": phone},
        {
            "$set": {
                "pin": pin,
                "updated_at": datetime.utcnow()
            }
        }
    )
    return {"message": "PIN updated successfully"}
