from fastapi import APIRouter, Depends, HTTPException
from modules.users.user_models import UserOut, UpdateUserModel
from utils.auth_utils import get_current_user_from_token
from database import db

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def get_my_profile(user: dict = Depends(get_current_user_from_token)):
    return user


@router.patch("/update", response_model=UserOut)
async def update_my_profile(
    updates: UpdateUserModel,
    current_user: dict = Depends(get_current_user_from_token)
):
    user_id = current_user["_id"]
    users_collection = db["users"]

    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": {k: v for k, v in updates.dict(exclude_unset=True).items()}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made or user not found")

    updated_user = await users_collection.find_one({"_id": user_id})
    return updated_user
