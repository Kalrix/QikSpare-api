from fastapi import APIRouter, Depends, HTTPException
from modules.auth.auth_models import OTPRequest, OTPVerify, RegisterUser, PINLogin
from modules.auth.auth_service import request_otp, verify_otp, register_user, login_with_pin
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
        # Route remains the same, internal logic handles auto-register
        token = await verify_otp(payload.phone, payload.otp, payload.session_id, payload.role, db)
        return {"token": token}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="OTP verification failed")


@router.post("/register-user")
async def register_new_user(payload: RegisterUser, db=Depends(get_database)):
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
