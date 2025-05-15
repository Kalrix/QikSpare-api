from datetime import datetime
from typing import Optional, List, Literal, Union
from pydantic import BaseModel, EmailStr, Field


# ----------- Shared Sub-Models -----------

class Location(BaseModel):
    addressLine: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class KYCDetails(BaseModel):
    driving_license: Optional[str] = None
    rc_book: Optional[str] = None
    fitness_certificate: Optional[str] = None
    insurance: Optional[str] = None
    documents: List[str] = []


# ----------- Base User Model -----------

class BaseUser(BaseModel):
    full_name: str
    phone: str
    role: Literal["admin", "vendor", "garage", "delivery"]

    email: Optional[EmailStr] = None
    pin: Optional[str] = None

    referral_code: Optional[str] = None
    referred_by: Optional[str] = None
    referral_count: int = 0
    referral_users: List[str] = []

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ----------- Role Specific Models -----------

class AdminUser(BaseUser):
    pass


class VendorUser(BaseUser):
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    gstin: Optional[str] = None
    pan_number: Optional[str] = None
    distributor_size: Optional[str] = None

    brands_carried: List[str] = []
    category_focus: List[str] = []

    kyc_status: Optional[str] = "optional"
    documents: List[str] = []

    location: Optional[Location] = None
    addresses: List[Location] = []


class GarageUser(BaseUser):
    garage_name: Optional[str] = None
    garage_size: Optional[str] = None

    brands_served: List[str] = []
    vehicle_types: List[str] = []
    category_focus: List[str] = []

    gstin: Optional[str] = None
    pan_number: Optional[str] = None

    kyc_status: Optional[str] = "optional"
    documents: List[str] = []

    location: Optional[Location] = None
    addresses: List[Location] = []


class DeliveryUser(BaseUser):
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    warehouse_assigned: Optional[str] = None

    kyc_details: Optional[KYCDetails] = None
    location: Optional[Location] = None

# ----------- Response Model -----------

class UserOut(BaseUser):
    # Flattened common fields for frontend consumption
    email: Optional[EmailStr] = None
    location: Optional[Location] = None
    addresses: Optional[List[Location]] = None
    documents: Optional[List[str]] = None
    kyc_status: Optional[str] = None
    gstin: Optional[str] = None
    pan_number: Optional[str] = None
    business_name: Optional[str] = None
    garage_name: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    warehouse_assigned: Optional[str] = None
    kyc_details: Optional[KYCDetails] = None
    brands_served: Optional[List[str]] = None
    brands_carried: Optional[List[str]] = None
    vehicle_types: Optional[List[str]] = None
    category_focus: Optional[List[str]] = None


# ----------- Update Schema (PATCH Support) -----------

class UpdateUserModel(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    pin: Optional[str] = None

    business_name: Optional[str] = None
    business_type: Optional[str] = None
    garage_name: Optional[str] = None
    gstin: Optional[str] = None
    pan_number: Optional[str] = None
    distributor_size: Optional[str] = None
    brands_served: Optional[List[str]] = None
    brands_carried: Optional[List[str]] = None
    vehicle_types: Optional[List[str]] = None
    category_focus: Optional[List[str]] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    warehouse_assigned: Optional[str] = None
    kyc_status: Optional[str] = None
    kyc_details: Optional[KYCDetails] = None
    documents: Optional[List[str]] = None

    location: Optional[Location] = None
    addresses: Optional[List[Location]] = None

    updated_at: Optional[datetime] = None



# ----------- Database Internal Model -----------

class UserInDB(BaseUser):
    id: Optional[str] = Field(alias="_id")


# ----------- Factory to Create Typed User -----------

def create_user_model(data: dict) -> Union[AdminUser, VendorUser, GarageUser, DeliveryUser]:
    role = data.get("role")
    if role == "admin":
        return AdminUser(**data)
    elif role == "vendor":
        return VendorUser(**data)
    elif role == "garage":
        return GarageUser(**data)
    elif role == "delivery":
        return DeliveryUser(**data)
    else:
        raise ValueError("Invalid user role")
