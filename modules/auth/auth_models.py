# modules/auth/auth_models.py

from pydantic import BaseModel, Field
from typing import Literal


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    otp: str
    session_id: str
    role: Literal["garage", "vendor"]


class PINLogin(BaseModel):
    phone: str
    pin: str


class RegisterUser(BaseModel):
    full_name: str
    phone: str
    role: Literal["garage", "vendor", "delivery"]
    pin: str


# ✅ NEW MODEL FOR PIN UPDATE
class UpdatePIN(BaseModel):
    phone: str
    pin: str  # 4-digit PIN
