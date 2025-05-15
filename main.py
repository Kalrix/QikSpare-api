from fastapi import FastAPI
from database import connect_to_mongo
from modules.auth.auth_routes import router as auth_router
from modules.users.user_routes import router as user_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    connect_to_mongo()

# Mount API routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/admin/users", tags=["Users"])
