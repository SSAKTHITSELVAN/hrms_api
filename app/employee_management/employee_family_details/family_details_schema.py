from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# =========================
# BASE SCHEMA
# =========================

class FamilyDetailsBase(BaseModel):
    employee_id: str = Field(..., description="Foreign Key to Employee")

    # Father
    is_father: Optional[bool] = Field(False, description="Whether father details are provided")
    father_name: Optional[str] = Field(None, max_length=100, description="Father's full name")
    father_date_of_birth: Optional[date] = Field(None, description="Father's birth date")
    father_contact_number: Optional[str] = Field(
        None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$',
        description="Father's contact number"
    )

    # Mother
    is_mother: Optional[bool] = Field(False, description="Whether mother details are provided")
    mother_name: Optional[str] = Field(None, max_length=100, description="Mother's full name")
    mother_date_of_birth: Optional[date] = Field(None, description="Mother's birth date")
    mother_contact_number: Optional[str] = Field(
        None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$',
        description="Mother's contact number"
    )

    # Spouse
    is_spouse: Optional[bool] = Field(False, description="Whether spouse details are provided")
    spouse_name: Optional[str] = Field(None, max_length=100, description="Spouse's full name")
    spouse_date_of_birth: Optional[date] = Field(None, description="Spouse's birth date")
    spouse_contact_number: Optional[str] = Field(
        None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$',
        description="Spouse's contact number"
    )

    # Children
    is_children: Optional[bool] = Field(False, description="Whether children details are provided")
    children_name: Optional[str] = Field(None, max_length=100, description="Children's name(s)")

    # Siblings
    is_siblings: Optional[bool] = Field(False, description="Whether sibling details are provided")
    sibling_names: Optional[str] = Field(None, max_length=100, description="Sibling name(s)")

# =========================
# CREATE SCHEMA
# =========================

class FamilyDetailsCreate(FamilyDetailsBase):
    """
    Schema for creating Family Details
    """
    pass

# =========================
# UPDATE SCHEMA
# =========================

class FamilyDetailsUpdate(BaseModel):
    """
    Schema for updating Family Details
    """
    # Make all fields optional for PATCH-like updates
    employee_id: Optional[str] = None

    is_father: Optional[bool] = None
    father_name: Optional[str] = Field(None, max_length=100)
    father_date_of_birth: Optional[date] = None
    father_contact_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$')

    is_mother: Optional[bool] = None
    mother_name: Optional[str] = Field(None, max_length=100)
    mother_date_of_birth: Optional[date] = None
    mother_contact_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$')

    is_spouse: Optional[bool] = None
    spouse_name: Optional[str] = Field(None, max_length=100)
    spouse_date_of_birth: Optional[date] = None
    spouse_contact_number: Optional[str] = Field(None, max_length=20, pattern=r'^\+?[\d\s\-\(\)]{10,20}$')

    is_children: Optional[bool] = None
    children_name: Optional[str] = Field(None, max_length=100)

    is_siblings: Optional[bool] = None
    sibling_names: Optional[str] = Field(None, max_length=100)

# =========================
# RESPONSE SCHEMA
# =========================

class FamilyDetailsResponse(FamilyDetailsBase):
    family_details_id: str = Field(..., description="Primary key of Family Details")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # For Pydantic v2 support