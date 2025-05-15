from pydantic import BaseModel, Field
from typing import Literal, Optional

class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class PINLogin(BaseModel):
    phone: str
    pin: str

class RegisterUser(BaseModel):
    full_name: str
    phone: str
    role: Literal["garage", "vendor", "delivery"]
    pin: str  # 4 digit PIN
