from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# =========================
# BASE SCHEMA
# =========================

class WorkExperienceBase(BaseModel):
    employee_id: Optional[str] = Field(None, description="Foreign Key to Employee")
    company_name: str = Field(..., max_length=255, description="Previous employer name")
    job_title: str = Field(..., max_length=255, description="Position held")
    start_date: date = Field(..., description="Employment start date")
    end_date: Optional[date] = Field(None, description="Employment end date (null if current)")
    responsibilities: Optional[str] = Field(None, description="Job responsibilities")
    achievements: Optional[str] = Field(None, description="Key achievements")
    location: Optional[str] = Field(None, max_length=255, description="Job location")
    reference_name: Optional[str] = Field(None, max_length=255, description="Reference person's name")
    reference_contact: Optional[str] = Field(None, max_length=20, description="Reference contact information")

class WorkExperienceCreate(WorkExperienceBase):
    """
    Schema for creating Work Experience
    """
    pass

class WorkExperienceUpdate(BaseModel):
    """
    Schema for updating Work Experience
    """
    company_name: Optional[str] = Field(None, max_length=255, description="Previous employer name")
    job_title: Optional[str] = Field(None, max_length=255, description="Position held")
    start_date: Optional[date] = Field(None, description="Employment start date")
    end_date: Optional[date] = Field(None, description="Employment end date (null if current)")
    responsibilities: Optional[str] = Field(None, description="Job responsibilities")
    achievements: Optional[str] = Field(None, description="Key achievements")
    location: Optional[str] = Field(None, max_length=255, description="Job location")
    reference_name: Optional[str] = Field(None, max_length=255, description="Reference person's name")
    reference_contact: Optional[str] = Field(None, max_length=20, description="Reference contact information")

class WorkExperienceResponse(WorkExperienceBase):
    experience_id: str  # Include primary key in the response
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Correct for Pydantic v2