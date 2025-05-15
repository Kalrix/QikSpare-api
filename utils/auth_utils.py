from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Dict
from config import JWT_SECRET

# Constants
ALGORITHM = "HS256"

# Define the OAuth2 scheme (used for dependency injection)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Placeholder, required by FastAPI

# -----------------------------
# Decode JWT and return payload
# -----------------------------
def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload  # Returns a dict with user_id, phone, role, etc.
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ---------------------------------
# Admin-only wrapper using JWT role
# ---------------------------------
async def get_current_admin_user(token: str = Depends(oauth2_scheme)) -> Dict:
    user = get_current_user_from_token(token)
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user
