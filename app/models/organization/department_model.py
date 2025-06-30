import uuid
import datetime
import enum
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Date, Time, DECIMAL, JSON, ForeignKey, Text, Enum as SqlAlchemyEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
# Make sure you import Base from your base module (assuming your project has it like before)


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
# DEPARTMENT MODEL
# =========================

class Department(Base):
    __tablename__ = "Department"

    department_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Company Foreign Key
    company_id = Column(String(36), ForeignKey("Company.company_id"), nullable=False)
    # company = relationship("Company", back_populates="departments")

    department_code = Column(String(20), nullable=False)
    department_name = Column(String(100), nullable=False)
    department_description = Column(Text, nullable=True)

    # Self Referencing FK: parent department
    parent_department_id = Column(String(36), ForeignKey("Department.department_id"), nullable=True)
    # parent_department = relationship("Department", remote_side=[department_id], backref="sub_departments")

    # Employee related FKs
    # department_head_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # department_deputy_head_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # department_hr_representative_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)

    # department_head = relationship("Employee", foreign_keys=[department_head_id])
    # department_deputy_head = relationship("Employee", foreign_keys=[department_deputy_head_id])
    # department_hr_representative = relationship("Employee", foreign_keys=[department_hr_representative_id])

    department_employee_count = Column(Integer, default=0)
    max_employee_capacity = Column(Integer, nullable=True)
    cost_center_code = Column(String(50), nullable=True)
    department_budget = Column(DECIMAL(15, 2), nullable=True)
    department_location = Column(String(200), nullable=True)
    department_phone = Column(String(20), nullable=True)
    department_email = Column(String(200), nullable=True)

    department_type = Column(SqlAlchemyEnum(DepartmentType), nullable=False, default=DepartmentType.OPERATIONAL)

    # Attendance & Leave Management
    working_hours_start = Column(Time, default=datetime.time(9, 0, 0))
    working_hours_end = Column(Time, default=datetime.time(17, 0, 0))
    break_duration_minutes = Column(Integer, default=60)
    flexible_hours_allowed = Column(Boolean, default=False)
    remote_work_allowed = Column(Boolean, default=False)
    overtime_allowed = Column(Boolean, default=True)
    weekend_work_required = Column(Boolean, default=False)

    # leave_approver_level_1_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # leave_approver_level_2_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # leave_approver_level_3_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)

    # leave_approver_level_1 = relationship("Employee", foreign_keys=[leave_approver_level_1_id])
    # leave_approver_level_2 = relationship("Employee", foreign_keys=[leave_approver_level_2_id])
    # leave_approver_level_3 = relationship("Employee", foreign_keys=[leave_approver_level_3_id])

    auto_approve_leave_days = Column(Integer, default=0)
    max_consecutive_leave_days = Column(Integer, default=30)
    advance_leave_notice_days = Column(Integer, default=7)

    # attendance_approver_level_1_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # attendance_approver_level_2_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)

    # attendance_approver_level_1 = relationship("Employee", foreign_keys=[attendance_approver_level_1_id])
    # attendance_approver_level_2 = relationship("Employee", foreign_keys=[attendance_approver_level_2_id])

    late_arrival_grace_minutes = Column(Integer, default=15)
    early_departure_requires_approval = Column(Boolean, default=True)

    # Role & Permissions
    default_employee_role_id = Column(String(36), ForeignKey("Role.role_id"), nullable=True)
    # default_employee_role = relationship("Role")

    can_employees_view_others = Column(Boolean, default=False)
    can_employees_request_overtime = Column(Boolean, default=True)
    requires_manager_approval_for = Column(JSON, nullable=True)
    department_specific_permissions = Column(JSON, nullable=True)

    # Self-Service Dashboard
    show_department_calendar = Column(Boolean, default=True)
    show_department_announcements = Column(Boolean, default=True)
    show_team_directory = Column(Boolean, default=True)
    allow_profile_updates = Column(Boolean, default=True)

    # Audit & Activity
    track_login_activity = Column(Boolean, default=True)
    track_attendance_changes = Column(Boolean, default=True)
    track_leave_activities = Column(Boolean, default=True)
    track_profile_changes = Column(Boolean, default=True)
    audit_retention_days = Column(Integer, default=365)

    # Status & Dates
    department_status = Column(SqlAlchemyEnum(DepartmentStatus), nullable=False, default=DepartmentStatus.ACTIVE)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    last_restructure_date = Column(Date, nullable=True)

    # Financial & Operational
    is_billable_department = Column(Boolean, default=False)
    requires_timesheet = Column(Boolean, default=False)
    project_based_work = Column(Boolean, default=False)
    client_facing = Column(Boolean, default=False)

    # Notifications & Contact
    notification_email = Column(String(200), nullable=True)
    escalation_email = Column(String(200), nullable=True)
    emergency_contact_number = Column(String(20), nullable=True)

    # Compliance
    requires_background_check = Column(Boolean, default=False)
    confidentiality_level = Column(SqlAlchemyEnum(ConfidentialityLevel), nullable=False, default=ConfidentialityLevel.STANDARD)
    data_access_restrictions = Column(JSON, nullable=True)
    compliance_requirements = Column(JSON, nullable=True)

    # System Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, default=1)

    # created_by_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # updated_by_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)

    # created_by = relationship("Employee", foreign_keys=[created_by_id])
    # updated_by = relationship("Employee", foreign_keys=[updated_by_id])
