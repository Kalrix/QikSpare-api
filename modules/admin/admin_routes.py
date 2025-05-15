from fastapi import APIRouter, Depends, HTTPException
from database import get_database
from modules.auth.auth_service import register_user
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

class AdminCreate(BaseModel):
    full_name: str
    phone: str
    role: Literal["admin"]
    pin: str

@router.post("/create-user")
async def create_admin(payload: AdminCreate, db=Depends(get_database)):
    user_dict = payload.dict()
    user_dict["referral_count"] = 0
    user_dict["referral_users"] = []
    user_dict["created_at"] = None
    user_dict["updated_at"] = None
    user_id = await register_user(user_dict, db)
    return {"message": "Admin created", "user_id": user_id}
