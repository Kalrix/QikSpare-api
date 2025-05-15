from fastapi import APIRouter, Depends, Request
from modules.users import user_service

router = APIRouter()

@router.post("/")
async def create_user(request: Request, data: dict):
    db = request.app.database
    user = await user_service.create_user(db, data)
    return {"message": "User created", "user": user}

@router.get("/")
async def get_all_users(request: Request):
    db = request.app.database
    users = await user_service.get_all_users(db)
    return {"users": users}

@router.get("/{user_id}")
async def get_user(user_id: str, request: Request):
    db = request.app.database
    return await user_service.get_user_by_id(db, user_id)

@router.patch("/{user_id}")
async def update_user(user_id: str, request: Request, data: dict):
    db = request.app.database
    return await user_service.update_user(db, user_id, data)

@router.delete("/{user_id}")
async def delete_user(user_id: str, request: Request):
    db = request.app.database
    return await user_service.delete_user(db, user_id)
