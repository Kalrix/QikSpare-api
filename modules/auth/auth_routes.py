from fastapi import APIRouter, Depends
from modules.auth.auth_models import OTPRequest, OTPVerify, RegisterUser, PINLogin
from modules.auth.auth_service import request_otp, verify_otp, register_user, login_with_pin
from database import get_database

router = APIRouter()

@router.post("/request-otp")
async def send_otp(payload: OTPRequest, db=Depends(get_database)):
    result = await request_otp(payload.phone, db)
    return {"message": "OTP sent", "session_id": result["session_id"]}

@router.post("/verify-otp")
async def verify_user_otp(payload: OTPVerify, db=Depends(get_database)):
    token = await verify_otp(payload.phone, payload.otp, payload.session_id, db)
    return {"token": token}

@router.post("/register-user")
async def register_new_user(payload: RegisterUser, db=Depends(get_database)):
    user_dict = payload.dict()
    user_dict["referral_count"] = 0
    user_dict["referral_users"] = []
    user_dict["created_at"] = user_dict["updated_at"] = None
    user_id = await register_user(user_dict, db)
    return {"message": "User created", "user_id": user_id}

@router.post("/login-pin")
async def login_user_with_pin(payload: PINLogin, db=Depends(get_database)):
    token = await login_with_pin(payload.phone, payload.pin, db)
    return {"token": token}
