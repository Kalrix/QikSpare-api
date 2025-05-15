from fastapi import FastAPI
from database import connect_to_mongo
from modules.auth import auth_routes
from modules.users import user_routes

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    connect_to_mongo()

# Mount your routes
app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(user_routes.router, prefix="/api/admin/users")
