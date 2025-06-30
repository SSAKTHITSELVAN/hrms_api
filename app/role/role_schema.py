from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


# Shared Base Schema
class RoleBase(BaseModel):
    company_id: str = Field(..., description="Foreign key for Company")
    role_name: str = Field(..., max_length=100, description="Name of the role")
    role_code: Optional[str] = Field(None, max_length=50, description="Optional code for role")
    role_description: Optional[str] = Field(None, description="Description of the role")
    is_system_role: Optional[bool] = Field(False, description="If role is system-defined")
    is_active: Optional[bool] = Field(True, description="Is role active")

    # Employee Management Permissions
    can_create_employee: Optional[bool] = False
    can_view_all_employees: Optional[bool] = False
    can_view_own_profile: Optional[bool] = False
    can_view_team_members: Optional[bool] = False
    can_view_department_employees: Optional[bool] = False
    can_edit_all_employee_profiles: Optional[bool] = False
    can_edit_own_profile: Optional[bool] = False
    can_edit_team_profiles: Optional[bool] = False
    can_delete_employee: Optional[bool] = False
    can_archive_employee: Optional[bool] = False
    can_restore_employee: Optional[bool] = False
    can_activate_employee: Optional[bool] = False
    can_deactivate_employee: Optional[bool] = False
    can_suspend_employee: Optional[bool] = False
    can_view_employee_documents: Optional[bool] = False
    can_upload_employee_documents: Optional[bool] = False
    can_delete_employee_documents: Optional[bool] = False

    # Attendance Management Permissions
    can_checkin_own: Optional[bool] = False
    can_checkout_own: Optional[bool] = False
    can_start_break_own: Optional[bool] = False
    can_end_break_own: Optional[bool] = False
    can_view_own_attendance: Optional[bool] = False
    can_view_team_attendance: Optional[bool] = False
    can_view_department_attendance: Optional[bool] = False
    can_view_all_attendance: Optional[bool] = False
    can_edit_own_attendance: Optional[bool] = False
    can_edit_team_attendance: Optional[bool] = False
    can_edit_all_attendance: Optional[bool] = False
    can_delete_attendance: Optional[bool] = False
    can_approve_attendance: Optional[bool] = False
    can_reject_attendance: Optional[bool] = False

    # Leave Management Permissions
    can_apply_own_leave: Optional[bool] = False
    can_apply_leave_behalf: Optional[bool] = False
    can_cancel_own_leave: Optional[bool] = False
    can_cancel_team_leave: Optional[bool] = False
    can_view_own_leave: Optional[bool] = False
    can_view_team_leave: Optional[bool] = False
    can_view_department_leave: Optional[bool] = False
    can_view_all_leave: Optional[bool] = False
    can_approve_team_leave: Optional[bool] = False
    can_approve_department_leave: Optional[bool] = False
    can_approve_all_leave: Optional[bool] = False
    can_reject_team_leave: Optional[bool] = False
    can_reject_department_leave: Optional[bool] = False
    can_reject_all_leave: Optional[bool] = False
    can_edit_own_leave: Optional[bool] = False
    can_edit_team_leave: Optional[bool] = False
    can_edit_all_leave: Optional[bool] = False
    can_delete_leave_records: Optional[bool] = False
    can_create_leave_types: Optional[bool] = False
    can_edit_leave_types: Optional[bool] = False
    can_delete_leave_types: Optional[bool] = False
    can_manage_leave_policies: Optional[bool] = False
    can_view_all_leave_balances: Optional[bool] = False

    # Department Management Permissions
    can_create_department: Optional[bool] = False
    can_view_all_departments: Optional[bool] = False
    can_view_own_department: Optional[bool] = False
    can_edit_all_departments: Optional[bool] = False
    can_edit_own_department: Optional[bool] = False
    can_delete_department: Optional[bool] = False
    can_assign_employees_department: Optional[bool] = False
    can_remove_employees_department: Optional[bool] = False
    can_transfer_employees: Optional[bool] = False
    can_manage_department_hierarchy: Optional[bool] = False
    can_assign_department_head: Optional[bool] = False

    # Role & Permission Management
    can_create_roles: Optional[bool] = False
    can_view_all_roles: Optional[bool] = False
    can_edit_all_roles: Optional[bool] = False
    can_delete_roles: Optional[bool] = False
    can_assign_roles: Optional[bool] = False
    can_unassign_roles: Optional[bool] = False

    # Company & Org Management
    can_view_company_details: Optional[bool] = False
    can_edit_company_details: Optional[bool] = False
    can_manage_company_settings: Optional[bool] = False
    can_view_org_hierarchy: Optional[bool] = False
    can_manage_org_hierarchy: Optional[bool] = False

    # Reporting & Analytics
    can_generate_employee_reports: Optional[bool] = False
    can_generate_attendance_reports: Optional[bool] = False
    can_generate_leave_reports: Optional[bool] = False
    can_generate_department_reports: Optional[bool] = False
    can_create_custom_reports: Optional[bool] = False

    # Data Export
    can_export_employee_data: Optional[bool] = False
    can_export_attendance_data: Optional[bool] = False
    can_export_leave_data: Optional[bool] = False
    can_export_all_data: Optional[bool] = False

    # Dashboard Access
    can_view_employee_dashboard: Optional[bool] = False
    can_view_attendance_dashboard: Optional[bool] = False
    can_view_leave_dashboard: Optional[bool] = False
    can_view_executive_dashboard: Optional[bool] = False

    # Audit & System Admin
    can_view_all_audit_logs: Optional[bool] = False
    can_view_own_audit_logs: Optional[bool] = False
    can_view_team_audit_logs: Optional[bool] = False
    can_export_audit_logs: Optional[bool] = False
    can_manage_system_settings: Optional[bool] = False
    can_create_system_backup: Optional[bool] = False
    can_restore_system_backup: Optional[bool] = False
    can_enable_maintenance_mode: Optional[bool] = False
    can_create_user_accounts: Optional[bool] = False
    can_edit_user_accounts: Optional[bool] = False
    can_delete_user_accounts: Optional[bool] = False
    can_reset_user_passwords: Optional[bool] = False
    can_lock_user_accounts: Optional[bool] = False
    can_unlock_user_accounts: Optional[bool] = False


# Create Schema
class RoleCreate(RoleBase):
    pass


# Update Schema
class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
    role_code: Optional[str] = None
    role_description: Optional[str] = None
    is_system_role: Optional[bool] = None
    is_active: Optional[bool] = None
    
    # Employee Management Permissions
    can_create_employee: Optional[bool] = False
    can_view_all_employees: Optional[bool] = False
    can_view_own_profile: Optional[bool] = False
    can_view_team_members: Optional[bool] = False
    can_view_department_employees: Optional[bool] = False
    can_edit_all_employee_profiles: Optional[bool] = False
    can_edit_own_profile: Optional[bool] = False
    can_edit_team_profiles: Optional[bool] = False
    can_delete_employee: Optional[bool] = False
    can_archive_employee: Optional[bool] = False
    can_restore_employee: Optional[bool] = False
    can_activate_employee: Optional[bool] = False
    can_deactivate_employee: Optional[bool] = False
    can_suspend_employee: Optional[bool] = False
    can_view_employee_documents: Optional[bool] = False
    can_upload_employee_documents: Optional[bool] = False
    can_delete_employee_documents: Optional[bool] = False

    # Attendance Management Permissions
    can_checkin_own: Optional[bool] = False
    can_checkout_own: Optional[bool] = False
    can_start_break_own: Optional[bool] = False
    can_end_break_own: Optional[bool] = False
    can_view_own_attendance: Optional[bool] = False
    can_view_team_attendance: Optional[bool] = False
    can_view_department_attendance: Optional[bool] = False
    can_view_all_attendance: Optional[bool] = False
    can_edit_own_attendance: Optional[bool] = False
    can_edit_team_attendance: Optional[bool] = False
    can_edit_all_attendance: Optional[bool] = False
    can_delete_attendance: Optional[bool] = False
    can_approve_attendance: Optional[bool] = False
    can_reject_attendance: Optional[bool] = False

    # Leave Management Permissions
    can_apply_own_leave: Optional[bool] = False
    can_apply_leave_behalf: Optional[bool] = False
    can_cancel_own_leave: Optional[bool] = False
    can_cancel_team_leave: Optional[bool] = False
    can_view_own_leave: Optional[bool] = False
    can_view_team_leave: Optional[bool] = False
    can_view_department_leave: Optional[bool] = False
    can_view_all_leave: Optional[bool] = False
    can_approve_team_leave: Optional[bool] = False
    can_approve_department_leave: Optional[bool] = False
    can_approve_all_leave: Optional[bool] = False
    can_reject_team_leave: Optional[bool] = False
    can_reject_department_leave: Optional[bool] = False
    can_reject_all_leave: Optional[bool] = False
    can_edit_own_leave: Optional[bool] = False
    can_edit_team_leave: Optional[bool] = False
    can_edit_all_leave: Optional[bool] = False
    can_delete_leave_records: Optional[bool] = False
    can_create_leave_types: Optional[bool] = False
    can_edit_leave_types: Optional[bool] = False
    can_delete_leave_types: Optional[bool] = False
    can_manage_leave_policies: Optional[bool] = False
    can_view_all_leave_balances: Optional[bool] = False

    # Department Management Permissions
    can_create_department: Optional[bool] = False
    can_view_all_departments: Optional[bool] = False
    can_view_own_department: Optional[bool] = False
    can_edit_all_departments: Optional[bool] = False
    can_edit_own_department: Optional[bool] = False
    can_delete_department: Optional[bool] = False
    can_assign_employees_department: Optional[bool] = False
    can_remove_employees_department: Optional[bool] = False
    can_transfer_employees: Optional[bool] = False
    can_manage_department_hierarchy: Optional[bool] = False
    can_assign_department_head: Optional[bool] = False

    # Role & Permission Management
    can_create_roles: Optional[bool] = False
    can_view_all_roles: Optional[bool] = False
    can_edit_all_roles: Optional[bool] = False
    can_delete_roles: Optional[bool] = False
    can_assign_roles: Optional[bool] = False
    can_unassign_roles: Optional[bool] = False

    # Company & Org Management
    can_view_company_details: Optional[bool] = False
    can_edit_company_details: Optional[bool] = False
    can_manage_company_settings: Optional[bool] = False
    can_view_org_hierarchy: Optional[bool] = False
    can_manage_org_hierarchy: Optional[bool] = False

    # Reporting & Analytics
    can_generate_employee_reports: Optional[bool] = False
    can_generate_attendance_reports: Optional[bool] = False
    can_generate_leave_reports: Optional[bool] = False
    can_generate_department_reports: Optional[bool] = False
    can_create_custom_reports: Optional[bool] = False

    # Data Export
    can_export_employee_data: Optional[bool] = False
    can_export_attendance_data: Optional[bool] = False
    can_export_leave_data: Optional[bool] = False
    can_export_all_data: Optional[bool] = False

    # Dashboard Access
    can_view_employee_dashboard: Optional[bool] = False
    can_view_attendance_dashboard: Optional[bool] = False
    can_view_leave_dashboard: Optional[bool] = False
    can_view_executive_dashboard: Optional[bool] = False

    # Audit & System Admin
    can_view_all_audit_logs: Optional[bool] = False
    can_view_own_audit_logs: Optional[bool] = False
    can_view_team_audit_logs: Optional[bool] = False
    can_export_audit_logs: Optional[bool] = False
    can_manage_system_settings: Optional[bool] = False
    can_create_system_backup: Optional[bool] = False
    can_restore_system_backup: Optional[bool] = False
    can_enable_maintenance_mode: Optional[bool] = False
    can_create_user_accounts: Optional[bool] = False
    can_edit_user_accounts: Optional[bool] = False
    can_delete_user_accounts: Optional[bool] = False
    can_reset_user_passwords: Optional[bool] = False
    can_lock_user_accounts: Optional[bool] = False
    can_unlock_user_accounts: Optional[bool] = False




# Response Schema
class RoleResponse(RoleBase):
    role_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # for pydantic v2

