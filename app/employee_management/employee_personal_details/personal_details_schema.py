from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from datetime import datetime
import enum



# =========================
# ENUM DEFINITIONS
# =========================

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    OTHER = "other"

class BloodGroup(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
    UNKNOWN = "unknown"



# =========================
# BASE SCHEMA
# =========================

class PersonalDetailsBase(BaseModel):
    employee_id: Optional[str] = Field(None, description="Foreign Key to Employee")
    first_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., max_length=100)
    gender: Optional[Gender]
    date_of_birth: Optional[date]
    marital_status: Optional[MaritalStatus]
    nationality: Optional[str] = Field(None, max_length=50)
    blood_group: Optional[BloodGroup]
    personal_contact_number: Optional[str] = Field(None, max_length=20)
    personal_email: Optional[EmailStr]
    permanent_address: Optional[str]
    current_address: Optional[str]
    emergency_contact_person: Optional[str] = Field(None, max_length=100)
    emergency_contact_number: Optional[str] = Field(None, max_length=20)



class PersonalDetailsCreate(PersonalDetailsBase):
    """
    Schema for creating Personal Details
    """
    pass




class PersonalDetailsUpdate(BaseModel):
    """
    Schema for updating Personal Details
    """
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    gender: Optional[Gender]
    date_of_birth: Optional[date]
    marital_status: Optional[MaritalStatus]
    nationality: Optional[str] = Field(None, max_length=50)
    blood_group: Optional[BloodGroup]
    personal_contact_number: Optional[str] = Field(None, max_length=20)
    personal_email: Optional[EmailStr]
    permanent_address: Optional[str]
    current_address: Optional[str]
    emergency_contact_person: Optional[str] = Field(None, max_length=100)
    emergency_contact_number: Optional[str] = Field(None, max_length=20)


class PersonalDetailsResponse(PersonalDetailsBase):
    employee_personal_details_id: str  # Include primary key in the response
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Correct for Pydantic v2
