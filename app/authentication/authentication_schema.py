from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import enum

# =========================
# ENUM DEFINITIONS
# =========================

class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

# =========================
# BASE SCHEMA
# =========================

class EmployeeBase(BaseModel):
    company_id: str = Field(..., max_length=36)
    employee_code: str = Field(..., description="Auto-generated unique login ID")
    employee_department_id: str = Field(..., max_length=36)
    employee_role_id: Optional[str] = Field(None, max_length=36)
    employee_hashed_password: str = Field(..., description="Hashed password")
    employee_status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE)
    employee_added_by: Optional[str] = Field(None, max_length=36)

# =========================
# CREATE SCHEMA
# =========================

class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new employee
    """
    pass

# =========================
# UPDATE SCHEMA
# =========================

class EmployeeUpdate(BaseModel):
    """
    Schema for updating an employee
    """
    company_id: Optional[str] = Field(None, max_length=36)
    employee_code: Optional[str] = Field(None)
    employee_department_id: Optional[str] = Field(None, max_length=36)
    employee_role_id: Optional[str] = Field(None, max_length=36)
    employee_hashed_password: Optional[str] = Field(None)
    employee_status: Optional[EmployeeStatus]
    employee_added_by: Optional[str] = Field(None, max_length=36)

# =========================
# RESPONSE SCHEMA
# =========================

class EmployeeResponse(EmployeeBase):
    employee_id: str
    employee_added_time: datetime
    employee_modified_time: datetime
    model_config = {"from_attributes": True}
