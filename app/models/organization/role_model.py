import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "Role"

    role_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    company_id = Column(String(36), ForeignKey("Company.company_id"), nullable=False)
    # company = relationship("Company", back_populates="roles")

    role_name = Column(String(100), nullable=False)
    role_code = Column(String(50), nullable=True)
    role_description = Column(Text, nullable=True)
    is_system_role = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Employee Management Permissions
    can_create_employee = Column(Boolean, default=False)
    can_view_all_employees = Column(Boolean, default=False)
    can_view_own_profile = Column(Boolean, default=False)
    can_view_team_members = Column(Boolean, default=False)
    can_view_department_employees = Column(Boolean, default=False)
    can_edit_all_employee_profiles = Column(Boolean, default=False)
    can_edit_own_profile = Column(Boolean, default=False)
    can_edit_team_profiles = Column(Boolean, default=False)
    can_delete_employee = Column(Boolean, default=False)
    can_archive_employee = Column(Boolean, default=False)
    can_restore_employee = Column(Boolean, default=False)
    can_activate_employee = Column(Boolean, default=False)
    can_deactivate_employee = Column(Boolean, default=False)
    can_suspend_employee = Column(Boolean, default=False)
    can_view_employee_documents = Column(Boolean, default=False)
    can_upload_employee_documents = Column(Boolean, default=False)
    can_delete_employee_documents = Column(Boolean, default=False)

    # Attendance Management Permissions
    can_checkin_own = Column(Boolean, default=False)
    can_checkout_own = Column(Boolean, default=False)
    can_start_break_own = Column(Boolean, default=False)
    can_end_break_own = Column(Boolean, default=False)
    can_view_own_attendance = Column(Boolean, default=False)
    can_view_team_attendance = Column(Boolean, default=False)
    can_view_department_attendance = Column(Boolean, default=False)
    can_view_all_attendance = Column(Boolean, default=False)
    can_edit_own_attendance = Column(Boolean, default=False)
    can_edit_team_attendance = Column(Boolean, default=False)
    can_edit_all_attendance = Column(Boolean, default=False)
    can_delete_attendance = Column(Boolean, default=False)
    can_approve_attendance = Column(Boolean, default=False)
    can_reject_attendance = Column(Boolean, default=False)

    # Leave Management Permissions
    can_apply_own_leave = Column(Boolean, default=False)
    can_apply_leave_behalf = Column(Boolean, default=False)
    can_cancel_own_leave = Column(Boolean, default=False)
    can_cancel_team_leave = Column(Boolean, default=False)
    can_view_own_leave = Column(Boolean, default=False)
    can_view_team_leave = Column(Boolean, default=False)
    can_view_department_leave = Column(Boolean, default=False)
    can_view_all_leave = Column(Boolean, default=False)
    can_approve_team_leave = Column(Boolean, default=False)
    can_approve_department_leave = Column(Boolean, default=False)
    can_approve_all_leave = Column(Boolean, default=False)
    can_reject_team_leave = Column(Boolean, default=False)
    can_reject_department_leave = Column(Boolean, default=False)
    can_reject_all_leave = Column(Boolean, default=False)
    can_edit_own_leave = Column(Boolean, default=False)
    can_edit_team_leave = Column(Boolean, default=False)
    can_edit_all_leave = Column(Boolean, default=False)
    can_delete_leave_records = Column(Boolean, default=False)
    can_create_leave_types = Column(Boolean, default=False)
    can_edit_leave_types = Column(Boolean, default=False)
    can_delete_leave_types = Column(Boolean, default=False)
    can_manage_leave_policies = Column(Boolean, default=False)
    can_view_all_leave_balances = Column(Boolean, default=False)

    # Department Management Permissions
    can_create_department = Column(Boolean, default=False)
    can_view_all_departments = Column(Boolean, default=False)
    can_view_own_department = Column(Boolean, default=False)
    can_edit_all_departments = Column(Boolean, default=False)
    can_edit_own_department = Column(Boolean, default=False)
    can_delete_department = Column(Boolean, default=False)
    can_assign_employees_department = Column(Boolean, default=False)
    can_remove_employees_department = Column(Boolean, default=False)
    can_transfer_employees = Column(Boolean, default=False)
    can_manage_department_hierarchy = Column(Boolean, default=False)
    can_assign_department_head = Column(Boolean, default=False)

    # Role & Permission Management Permissions
    can_create_roles = Column(Boolean, default=False)
    can_view_all_roles = Column(Boolean, default=False)
    can_edit_all_roles = Column(Boolean, default=False)
    can_delete_roles = Column(Boolean, default=False)
    can_assign_roles = Column(Boolean, default=False)
    can_unassign_roles = Column(Boolean, default=False)

    # Company & Organization Management Permissions
    can_view_company_details = Column(Boolean, default=False)
    can_edit_company_details = Column(Boolean, default=False)
    can_manage_company_settings = Column(Boolean, default=False)
    can_view_org_hierarchy = Column(Boolean, default=False)
    can_manage_org_hierarchy = Column(Boolean, default=False)

    # Reporting & Analytics Permissions
    can_generate_employee_reports = Column(Boolean, default=False)
    can_generate_attendance_reports = Column(Boolean, default=False)
    can_generate_leave_reports = Column(Boolean, default=False)
    can_generate_department_reports = Column(Boolean, default=False)
    can_create_custom_reports = Column(Boolean, default=False)

    # Data Export Permissions
    can_export_employee_data = Column(Boolean, default=False)
    can_export_attendance_data = Column(Boolean, default=False)
    can_export_leave_data = Column(Boolean, default=False)
    can_export_all_data = Column(Boolean, default=False)

    # Dashboard Access Permissions
    can_view_employee_dashboard = Column(Boolean, default=False)
    can_view_attendance_dashboard = Column(Boolean, default=False)
    can_view_leave_dashboard = Column(Boolean, default=False)
    can_view_executive_dashboard = Column(Boolean, default=False)

    # Audit & System Administration Permissions
    can_view_all_audit_logs = Column(Boolean, default=False)
    can_view_own_audit_logs = Column(Boolean, default=False)
    can_view_team_audit_logs = Column(Boolean, default=False)
    can_export_audit_logs = Column(Boolean, default=False)
    can_manage_system_settings = Column(Boolean, default=False)
    can_create_system_backup = Column(Boolean, default=False)
    can_restore_system_backup = Column(Boolean, default=False)
    can_enable_maintenance_mode = Column(Boolean, default=False)
    can_create_user_accounts = Column(Boolean, default=False)
    can_edit_user_accounts = Column(Boolean, default=False)
    can_delete_user_accounts = Column(Boolean, default=False)
    can_reset_user_passwords = Column(Boolean, default=False)
    can_lock_user_accounts = Column(Boolean, default=False)
    can_unlock_user_accounts = Column(Boolean, default=False)

    # System Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # created_by_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)
    # updated_by_id = Column(String(36), ForeignKey("Employee.employee_id"), nullable=True)

    # created_by = relationship("Employee", foreign_keys=[created_by_id])
    # updated_by = relationship("Employee", foreign_keys=[updated_by_id])

