from fastapi import APIRouter, Depends
from modules.users.user_service import get_all_users
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", tags=["Admin - Users"])
async def list_users():
    users = await get_all_users()
    return JSONResponse(content={"users": users})
