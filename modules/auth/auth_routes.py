# modules/auth/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException
from modules.auth.auth_models import (
    OTPRequest,
    OTPVerify,
    RegisterUser,
    PINLogin,
    UpdatePIN,
)
from modules.auth.auth_service import (
    request_otp,
    verify_otp,
    register_user,
    login_with_pin,
)
from database import get_database
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/request-otp")
async def send_otp(payload: OTPRequest, db=Depends(get_database)):
    session = await request_otp(payload.phone, db)
    return {"message": "OTP sent", "session_id": session["session_id"]}


@router.post("/verify-otp")
async def verify_user_otp(payload: OTPVerify, db=Depends(get_database)):
    try:
        token = await verify_otp(
            payload.phone, payload.otp, payload.session_id, payload.role, db
        )
        return {"token": token}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="OTP verification failed")


@router.post("/register-user")
async def register_new_user(payload: RegisterUser, db=Depends(get_database)):
    existing = await db["users"].find_one({"phone": payload.phone})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_dict = payload.dict()
    user_dict.update({
        "referral_count": 0,
        "referral_users": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    user_id = await register_user(user_dict, db)
    return {"message": "User created", "user_id": user_id}


@router.post("/login-pin")
async def login_user_with_pin(payload: PINLogin, db=Depends(get_database)):
    token = await login_with_pin(payload.phone, payload.pin, db)
    return {"token": token}


# ✅ NEW: Update PIN endpoint
@router.patch("/update-pin")
async def update_user_pin(payload: UpdatePIN, db=Depends(get_database)):
    user = await db["users"].find_one({"phone": payload.phone})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db["users"].update_one(
        {"phone": payload.phone},
        {
            "$set": {
                "pin": payload.pin,
                "updated_at": datetime.utcnow(),
            }
        }
    )

    return {"message": "PIN updated successfully"}
