from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any
from datetime import datetime, date, time
import enum


# =========================
# ENUM DEFINITIONS
# =========================

class DepartmentType(str, enum.Enum):
    OPERATIONAL = "operational"
    SUPPORT = "support"
    MANAGEMENT = "management"
    ADMINISTRATIVE = "administrative"

class DepartmentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    RESTRUCTURING = "restructuring"
    ARCHIVED = "archived"

class ConfidentialityLevel(str, enum.Enum):
    PUBLIC = "public"
    STANDARD = "standard"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


# =========================
# BASE SCHEMA
# =========================

class DepartmentBase(BaseModel):
    company_id: str = Field(..., description="FK to Company")
    department_code: str = Field(..., max_length=20)
    department_name: str = Field(..., max_length=100)
    department_description: Optional[str] = None

    parent_department_id: Optional[str] = None

    # department_head_id: Optional[str] = None
    # department_deputy_head_id: Optional[str] = None
    # department_hr_representative_id: Optional[str] = None

    department_employee_count: Optional[int] = 0
    max_employee_capacity: Optional[int] = None
    cost_center_code: Optional[str] = Field(None, max_length=50)
    department_budget: Optional[float] = None
    department_location: Optional[str] = Field(None, max_length=200)
    department_phone: Optional[str] = Field(None, max_length=20)
    department_email: Optional[EmailStr] = None

    department_type: DepartmentType = Field(default=DepartmentType.OPERATIONAL)

    # Attendance & Leave
    working_hours_start: Optional[time] = time(9, 0)
    working_hours_end: Optional[time] = time(17, 0)
    break_duration_minutes: Optional[int] = 60
    flexible_hours_allowed: Optional[bool] = False
    remote_work_allowed: Optional[bool] = False
    overtime_allowed: Optional[bool] = True
    weekend_work_required: Optional[bool] = False

    # leave_approver_level_1_id: Optional[str] = None
    # leave_approver_level_2_id: Optional[str] = None
    # leave_approver_level_3_id: Optional[str] = None

    auto_approve_leave_days: Optional[int] = 0
    max_consecutive_leave_days: Optional[int] = 30
    advance_leave_notice_days: Optional[int] = 7

    # attendance_approver_level_1_id: Optional[str] = None
    # attendance_approver_level_2_id: Optional[str] = None

    late_arrival_grace_minutes: Optional[int] = 15
    early_departure_requires_approval: Optional[bool] = True

    default_employee_role_id: Optional[str] = None

    can_employees_view_others: Optional[bool] = False
    can_employees_request_overtime: Optional[bool] = True
    requires_manager_approval_for: Optional[Any] = None  # JSON
    department_specific_permissions: Optional[Any] = None  # JSON

    show_department_calendar: Optional[bool] = True
    show_department_announcements: Optional[bool] = True
    show_team_directory: Optional[bool] = True
    allow_profile_updates: Optional[bool] = True

    track_login_activity: Optional[bool] = True
    track_attendance_changes: Optional[bool] = True
    track_leave_activities: Optional[bool] = True
    track_profile_changes: Optional[bool] = True
    audit_retention_days: Optional[int] = 365

    department_status: DepartmentStatus = Field(default=DepartmentStatus.ACTIVE)
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    last_restructure_date: Optional[date] = None

    is_billable_department: Optional[bool] = False
    requires_timesheet: Optional[bool] = False
    project_based_work: Optional[bool] = False
    client_facing: Optional[bool] = False

    notification_email: Optional[EmailStr] = None
    escalation_email: Optional[EmailStr] = None
    emergency_contact_number: Optional[str] = Field(None, max_length=20)

    requires_background_check: Optional[bool] = False
    confidentiality_level: ConfidentialityLevel = Field(default=ConfidentialityLevel.STANDARD)
    data_access_restrictions: Optional[Any] = None
    compliance_requirements: Optional[Any] = None


# =========================
# CREATE SCHEMA
# =========================

class DepartmentCreate(DepartmentBase):
    """
    Schema for creating a new department
    """
    pass


# =========================
# UPDATE SCHEMA
# =========================

class DepartmentUpdate(BaseModel):
    company_id: Optional[str] = None
    department_code: Optional[str] = Field(None, max_length=20)
    department_name: Optional[str] = Field(None, max_length=100)
    department_description: Optional[str] = None

    parent_department_id: Optional[str] = None

    # department_head_id: Optional[str] = None
    # department_deputy_head_id: Optional[str] = None
    # department_hr_representative_id: Optional[str] = None

    department_employee_count: Optional[int] = None
    max_employee_capacity: Optional[int] = None
    cost_center_code: Optional[str] = Field(None, max_length=50)
    department_budget: Optional[float] = None
    department_location: Optional[str] = Field(None, max_length=200)
    department_phone: Optional[str] = Field(None, max_length=20)
    department_email: Optional[EmailStr] = None

    department_type: Optional[DepartmentType] = None

    working_hours_start: Optional[time] = None
    working_hours_end: Optional[time] = None
    break_duration_minutes: Optional[int] = None
    flexible_hours_allowed: Optional[bool] = None
    remote_work_allowed: Optional[bool] = None
    overtime_allowed: Optional[bool] = None
    weekend_work_required: Optional[bool] = None

    # leave_approver_level_1_id: Optional[str] = None
    # leave_approver_level_2_id: Optional[str] = None
    # leave_approver_level_3_id: Optional[str] = None

    auto_approve_leave_days: Optional[int] = None
    max_consecutive_leave_days: Optional[int] = None
    advance_leave_notice_days: Optional[int] = None

    # attendance_approver_level_1_id: Optional[str] = None
    # attendance_approver_level_2_id: Optional[str] = None

    late_arrival_grace_minutes: Optional[int] = None
    early_departure_requires_approval: Optional[bool] = None

    default_employee_role_id: Optional[str] = None

    can_employees_view_others: Optional[bool] = None
    can_employees_request_overtime: Optional[bool] = None
    requires_manager_approval_for: Optional[Any] = None
    department_specific_permissions: Optional[Any] = None

    show_department_calendar: Optional[bool] = None
    show_department_announcements: Optional[bool] = None
    show_team_directory: Optional[bool] = None
    allow_profile_updates: Optional[bool] = None

    track_login_activity: Optional[bool] = None
    track_attendance_changes: Optional[bool] = None
    track_leave_activities: Optional[bool] = None
    track_profile_changes: Optional[bool] = None
    audit_retention_days: Optional[int] = None

    department_status: Optional[DepartmentStatus] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    last_restructure_date: Optional[date] = None

    is_billable_department: Optional[bool] = None
    requires_timesheet: Optional[bool] = None
    project_based_work: Optional[bool] = None
    client_facing: Optional[bool] = None

    notification_email: Optional[EmailStr] = None
    escalation_email: Optional[EmailStr] = None
    emergency_contact_number: Optional[str] = Field(None, max_length=20)

    requires_background_check: Optional[bool] = None
    confidentiality_level: Optional[ConfidentialityLevel] = None
    data_access_restrictions: Optional[Any] = None
    compliance_requirements: Optional[Any] = None


# =========================
# RESPONSE SCHEMA
# =========================

class DepartmentResponse(DepartmentBase):
    department_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    version: int

    # created_by_id: Optional[str]
    # updated_by_id: Optional[str]

    class Config:
        from_attributes = True  # <-- for SQLAlchemy ORM integration
