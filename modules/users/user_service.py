from database import db

async def get_all_users():
    users_cursor = db["users"].find()
    users = []
    async for user in users_cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users
