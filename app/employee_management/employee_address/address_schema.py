from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum

# =========================
# ENUM DEFINITIONS
# =========================

class AddressType(str, enum.Enum):
    PERMANENT = "permanent"
    CURRENT = "current"
    WORK = "work"

# =========================
# BASE SCHEMA
# =========================

class AddressBase(BaseModel):
    employee_id: Optional[str] = Field(None, description="Foreign Key to Employee")
    address_type: AddressType = Field(..., description="Type of address: permanent, current, work")
    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(..., max_length=100)
    is_current: Optional[bool] = Field(False, description="Is this the current address?")

# =========================
# CREATE SCHEMA
# =========================

class AddressCreate(AddressBase):
    """
    Schema for creating Address
    """
    pass

# =========================
# UPDATE SCHEMA
# =========================

class AddressUpdate(BaseModel):
    """
    Schema for updating Address
    """
    address_type: Optional[AddressType]
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    is_current: Optional[bool]

# =========================
# RESPONSE SCHEMA
# =========================

class AddressResponse(AddressBase):
    address_id: str  # Primary Key
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2 config
