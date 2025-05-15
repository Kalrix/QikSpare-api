from fastapi import FastAPI
from database import connect_to_mongo
from modules.auth.auth_routes import router as auth_router
from modules.users.user_routes import router as user_router
from modules.profile.profile_routes import router as profile_router
from modules.admin.admin_routes import router as admin_router


app = FastAPI(title="QikSpare Backend", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    connect_to_mongo()


# Mount API routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/admin/users", tags=["Users"])
app.include_router(profile_router, prefix="/api/profile", tags=["Profile"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

