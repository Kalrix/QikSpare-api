from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal, Union
from datetime import datetime


# -------------------- COMMON SCHEMAS --------------------

class Location(BaseModel):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class BankDetails(BaseModel):
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None
    beneficiary_name: Optional[str] = None
    upi_id: Optional[str] = None


class KYC(BaseModel):
    aadhaar: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    driving_license: Optional[str] = None
    rc_number: Optional[str] = None
    fitness_certificate: Optional[str] = None
    documents: List[dict] = []  # Can be {"type": "pan", "url": "..."}

# -------------------- BASE USER --------------------

class BaseUser(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    role: Literal["admin", "garage", "vendor", "delivery"]
    pin: Optional[str] = None  # 4-digit PIN for future login
    referral_code: Optional[str] = None
    referred_by: Optional[str] = None
    referral_count: int = 0
    referral_users: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# -------------------- ROLE-SPECIFIC FIELDS --------------------

class GarageProfile(BaseModel):
    garage_name: Optional[str] = None
    garage_size: Optional[str] = None
    brands_served: List[str] = []
    vehicle_types: List[str] = []
    category_focus: List[str] = []
    location: Optional[Location] = None
    kyc: Optional[KYC] = None

class VendorProfile(BaseModel):
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    distributor_size: Optional[str] = None
    brands_carried: List[str] = []
    category_focus: List[str] = []
    location: Optional[Location] = None
    kyc: Optional[KYC] = None
    bank_details: Optional[BankDetails] = None

class DeliveryProfile(BaseModel):
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    warehouse_assigned: Optional[str] = None
    location: Optional[Location] = None
    kyc: Optional[KYC] = None

# -------------------- COMBINED USER SCHEMA --------------------

class User(BaseUser):
    garage_profile: Optional[GarageProfile] = None
    vendor_profile: Optional[VendorProfile] = None
    delivery_profile: Optional[DeliveryProfile] = None

class UserInDB(User):
    id: Optional[str] = Field(alias="_id")
