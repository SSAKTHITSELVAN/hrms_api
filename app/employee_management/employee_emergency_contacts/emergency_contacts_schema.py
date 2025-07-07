from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class EmergencyContactBase(BaseModel):
    employee_id: Optional[str] = Field(None, description="Foreign Key to Employee")
    name: str = Field(..., max_length=100, description="Contact person's name")
    relationship: str = Field(..., max_length=50, description="Relationship to employee")
    primary_phone: str = Field(..., max_length=20, description="Primary contact number")
    secondary_phone: Optional[str] = Field(None, max_length=20, description="Alternative contact number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    address: Optional[str] = Field(None, description="Physical address")
    priority_order: int = Field(1, ge=1, le=10, description="Priority order (1 = primary contact)")


class EmergencyContactCreate(EmergencyContactBase):
    """
    Schema for creating Emergency Contact
    """
    pass


class EmergencyContactUpdate(BaseModel):
    """
    Schema for updating Emergency Contact
    """
    name: Optional[str] = Field(None, max_length=100, description="Contact person's name")
    relationship: Optional[str] = Field(None, max_length=50, description="Relationship to employee")
    primary_phone: Optional[str] = Field(None, max_length=20, description="Primary contact number")
    secondary_phone: Optional[str] = Field(None, max_length=20, description="Alternative contact number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    address: Optional[str] = Field(None, description="Physical address")
    priority_order: Optional[int] = Field(None, ge=1, le=10, description="Priority order (1 = primary contact)")


class EmergencyContactResponse(EmergencyContactBase):
    contact_id: str  # Include primary key in the response
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Correct for Pydantic v2