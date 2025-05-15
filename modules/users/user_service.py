from fastapi import HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from modules.users.user_models import create_user_model

def get_user_collection(db) -> Collection:
    return db["users"]

async def create_user(db, data: dict):
    user_collection = get_user_collection(db)
    existing = await user_collection.find_one({"phone": data["phone"]})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_model = create_user_model(data)
    user_dict = user_model.dict(by_alias=True)
    await user_collection.insert_one(user_dict)
    return user_dict

async def get_all_users(db):
    user_collection = get_user_collection(db)
    users = []
    async for user in user_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

async def get_user_by_id(db, user_id: str):
    user_collection = get_user_collection(db)
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

async def update_user(db, user_id: str, update_data: dict):
    user_collection = get_user_collection(db)
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed or no changes")
    return await get_user_by_id(db, user_id)

async def delete_user(db, user_id: str):
    user_collection = get_user_collection(db)
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
