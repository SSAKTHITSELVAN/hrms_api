from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# =========================
# BASE SCHEMA
# =========================

class EducationBase(BaseModel):
    employee_id: Optional[str] = Field(None, description="Foreign Key to Employee")

    institution_name: str = Field(..., max_length=255)
    institution_location: Optional[str] = Field(None, max_length=255)

    degree_name: str = Field(..., max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_level: str = Field(..., max_length=50, description="e.g., Bachelor, Master, Diploma")
    mode_of_study: Optional[str] = Field(None, max_length=50, description="Full-time, Part-time, Online, Distance")

    start_date: Optional[date]
    completion_date: Optional[date]

    percentage_or_grade: Optional[str] = Field(None, max_length=50)

    is_highest_qualification: Optional[bool] = Field(False)

    additional_notes: Optional[str]

# =========================
# CREATE SCHEMA
# =========================

class EducationCreate(EducationBase):
    """
    Schema for creating Education
    """
    pass

# =========================
# UPDATE SCHEMA
# =========================

class EducationUpdate(BaseModel):
    """
    Schema for updating Education
    """
    institution_name: Optional[str] = Field(None, max_length=255)
    institution_location: Optional[str] = Field(None, max_length=255)

    degree_name: Optional[str] = Field(None, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_level: Optional[str] = Field(None, max_length=50)
    mode_of_study: Optional[str] = Field(None, max_length=50)

    start_date: Optional[date]
    completion_date: Optional[date]

    percentage_or_grade: Optional[str] = Field(None, max_length=50)

    is_highest_qualification: Optional[bool]

    additional_notes: Optional[str]

# =========================
# RESPONSE SCHEMA
# =========================

class EducationResponse(EducationBase):
    education_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
