"""
HRMS Constants - Error Responses, Status Codes, and Messages
FastAPI HRMS Application Constants File
"""

from enum import Enum
from typing import Dict, Any

# HTTP Status Codes
class StatusCode:
    # Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    
    # Server Errors
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

# Response Messages
class ResponseMessage:
    # Generic Success Messages
    SUCCESS = "Operation completed successfully"
    CREATED_SUCCESS = "Resource created successfully"
    UPDATED_SUCCESS = "Resource updated successfully"
    DELETED_SUCCESS = "Resource deleted successfully"
    
    # Generic Error Messages
    INTERNAL_ERROR = "Internal server error occurred"
    INVALID_REQUEST = "Invalid request parameters"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    FORBIDDEN_ACCESS = "Access forbidden"
    RESOURCE_NOT_FOUND = "Requested resource not found"
    VALIDATION_ERROR = "Validation error in request data"



# Company Management Constants
class CompanyConstants:
    # Success Messages
    COMPANY_CREATED = "Company created successfully"
    COMPANY_UPDATED = "Company profile updated successfully"
    COMPANY_DELETED = "Company deleted successfully"
    COMPANY_RETRIEVED = "Company data retrieved successfully"
    COMPANIES_LIST_RETRIEVED = "Companies list retrieved successfully"
    COMPANY_ACTIVATED = "Company activated successfully"
    COMPANY_DEACTIVATED = "Company deactivated successfully"
    COMPANY_SETTINGS_UPDATED = "Company settings updated successfully"
    COMPANY_LOGO_UPLOADED = "Company logo uploaded successfully"
    COMPANY_LOGO_DELETED = "Company logo deleted successfully"
    
    # Error Messages
    COMPANY_NOT_FOUND = "Company not found"
    COMPANY_ALREADY_EXISTS = "Company with this name/registration number already exists"
    INVALID_COMPANY_ID = "Invalid company ID provided"
    COMPANY_HAS_EMPLOYEES = "Cannot delete company with existing employees"
    COMPANY_HAS_DEPARTMENTS = "Cannot delete company with existing departments"
    INVALID_COMPANY_DATA = "Invalid company data provided"
    COMPANY_EMAIL_EXISTS = "Company email address already registered"
    COMPANY_REGISTRATION_EXISTS = "Company registration number already exists"
    COMPANY_PHONE_EXISTS = "Company phone number already registered"
    COMPANY_INACTIVE = "Company is inactive"
    COMPANY_SUSPENDED = "Company account is suspended"
    INVALID_COMPANY_TYPE = "Invalid company type specified"
    COMPANY_LOGO_REQUIRED = "Company logo is required"
    INVALID_LOGO_FORMAT = "Invalid logo file format"
    LOGO_SIZE_EXCEEDED = "Logo file size exceeds maximum limit"
    COMPANY_ADDRESS_REQUIRED = "Company address is required"
    INVALID_REGISTRATION_NUMBER = "Invalid company registration number format"
    INVALID_TAX_ID = "Invalid tax identification number"
    COMPANY_LIMIT_EXCEEDED = "Maximum number of companies limit exceeded"


# Employee Data Management Constants
class EmployeeConstants:
    # Success Messages
    EMPLOYEE_CREATED = "Employee created successfully"
    EMPLOYEE_UPDATED = "Employee profile updated successfully"
    EMPLOYEE_DELETED = "Employee deleted successfully"
    EMPLOYEE_RETRIEVED = "Employee data retrieved successfully"
    EMPLOYEES_LIST_RETRIEVED = "Employees list retrieved successfully"
    
    # Error Messages
    EMPLOYEE_NOT_FOUND = "Employee not found"
    EMPLOYEE_ALREADY_EXISTS = "Employee with this email/ID already exists"
    INVALID_EMPLOYEE_ID = "Invalid employee ID provided"
    EMPLOYEE_CANNOT_DELETE_SELF = "Employee cannot delete their own account"
    EMPLOYEE_HAS_DEPENDENCIES = "Cannot delete employee with existing dependencies"
    INVALID_EMPLOYEE_DATA = "Invalid employee data provided"
    EMPLOYEE_EMAIL_EXISTS = "Email address already registered"
    EMPLOYEE_PHONE_EXISTS = "Phone number already registered"

# Attendance Management Constants
class AttendanceConstants:
    # Success Messages
    CHECK_IN_SUCCESS = "Check-in recorded successfully"
    CHECK_OUT_SUCCESS = "Check-out recorded successfully"
    BREAK_START_SUCCESS = "Break started successfully"
    BREAK_END_SUCCESS = "Break ended successfully"
    ATTENDANCE_UPDATED = "Attendance record updated successfully"
    ATTENDANCE_RETRIEVED = "Attendance data retrieved successfully"
    
    # Error Messages
    ALREADY_CHECKED_IN = "Employee already checked in today"
    NOT_CHECKED_IN = "Employee not checked in today"
    ALREADY_CHECKED_OUT = "Employee already checked out today"
    ALREADY_ON_BREAK = "Employee already on break"
    NOT_ON_BREAK = "Employee not currently on break"
    ATTENDANCE_NOT_FOUND = "Attendance record not found"
    INVALID_ATTENDANCE_TIME = "Invalid attendance time provided"
    FUTURE_DATE_NOT_ALLOWED = "Cannot mark attendance for future dates"
    ATTENDANCE_ALREADY_EXISTS = "Attendance already marked for this date"

# Leave Management Constants
class LeaveConstants:
    # Success Messages
    LEAVE_APPLIED = "Leave application submitted successfully"
    LEAVE_APPROVED = "Leave request approved successfully"
    LEAVE_REJECTED = "Leave request rejected successfully"
    LEAVE_CANCELLED = "Leave request cancelled successfully"
    LEAVE_UPDATED = "Leave request updated successfully"
    LEAVE_RETRIEVED = "Leave data retrieved successfully"
    
    # Error Messages
    LEAVE_NOT_FOUND = "Leave request not found"
    INSUFFICIENT_LEAVE_BALANCE = "Insufficient leave balance"
    LEAVE_ALREADY_APPROVED = "Leave request already approved"
    LEAVE_ALREADY_REJECTED = "Leave request already rejected"
    OVERLAPPING_LEAVE = "Leave request overlaps with existing approved leave"
    INVALID_LEAVE_DATES = "Invalid leave dates provided"
    PAST_DATE_NOT_ALLOWED = "Cannot apply leave for past dates"
    INVALID_LEAVE_TYPE = "Invalid leave type specified"
    UNAUTHORIZED_LEAVE_ACTION = "Unauthorized to perform this action on leave request"
    LEAVE_PERIOD_EXCEEDED = "Leave period exceeds maximum allowed duration"

# Role & Permission Management Constants
class RoleConstants:
    # Success Messages
    ROLE_RETRIEVED = "Role retrieved successfully"
    ROLE_CREATED = "Role created successfully"
    ROLE_UPDATED = "Role updated successfully"
    ROLE_DELETED = "Role deleted successfully"
    ROLE_ASSIGNED = "Role assigned to user successfully"
    PERMISSION_GRANTED = "Permission granted successfully"
    PERMISSION_REVOKED = "Permission revoked successfully"
    
    # Error Messages
    ROLE_NOT_FOUND = "Role not found"
    ROLE_ALREADY_EXISTS = "Role with this name already exists"
    ROLE_IN_USE = "Cannot delete role as it's assigned to users"
    PERMISSION_NOT_FOUND = "Permission not found"
    INVALID_ROLE_NAME = "Invalid role name provided"
    INSUFFICIENT_PERMISSIONS = "Insufficient permissions to perform this action"
    CANNOT_MODIFY_SUPER_ADMIN = "Cannot modify super admin role"

# Hierarchy Management Constants
class HierarchyConstants:
    # Success Messages
    HIERARCHY_CREATED = "Hierarchy relationship created successfully"
    HIERARCHY_UPDATED = "Hierarchy relationship updated successfully"
    HIERARCHY_DELETED = "Hierarchy relationship deleted successfully"
    MANAGER_ASSIGNED = "Manager assigned successfully"
    
    # Error Messages
    HIERARCHY_NOT_FOUND = "Hierarchy relationship not found"
    CIRCULAR_HIERARCHY = "Circular hierarchy relationship not allowed"
    INVALID_MANAGER = "Invalid manager assignment"
    MANAGER_NOT_FOUND = "Manager not found"
    SELF_REPORTING_NOT_ALLOWED = "Employee cannot report to themselves"
    HIERARCHY_ALREADY_EXISTS = "Hierarchy relationship already exists"

# Department Management Constants
class DepartmentConstants:
    # Success Messages
    DEPARTMENT_CREATED = "Department created successfully"
    DEPARTMENT_UPDATED = "Department updated successfully"
    DEPARTMENT_DELETED = "Department deleted successfully"
    DEPARTMENT_HEAD_ASSIGNED = "Department head assigned successfully"
    EMPLOYEE_ASSIGNED_TO_DEPT = "Employee assigned to department successfully"
    
    # Error Messages
    DEPARTMENT_NOT_FOUND = "Department not found"
    DEPARTMENT_ALREADY_EXISTS = "Department with this name already exists"
    DEPARTMENT_HAS_EMPLOYEES = "Cannot delete department with assigned employees"
    INVALID_DEPARTMENT_HEAD = "Invalid department head assignment"
    DEPARTMENT_HEAD_NOT_IN_DEPT = "Department head must be a member of the department"
    EMPLOYEE_ALREADY_IN_DEPT = "Employee already assigned to this department"

# Audit Logs Constants
class AuditConstants:
    # Success Messages
    AUDIT_LOG_RETRIEVED = "Audit logs retrieved successfully"
    ACTIVITY_LOG_RETRIEVED = "Activity logs retrieved successfully"
    
    # Error Messages
    AUDIT_LOG_NOT_FOUND = "Audit log not found"
    INVALID_DATE_RANGE = "Invalid date range for audit logs"
    AUDIT_ACCESS_DENIED = "Access denied to audit logs"

# Authentication & Authorization Constants
class AuthConstants:
    # Success Messages
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    PASSWORD_CHANGED = "Password changed successfully"
    PASSWORD_RESET = "Password reset successfully"
    TOKEN_REFRESHED = "Token refreshed successfully"
    
    # Error Messages
    INVALID_CREDENTIALS = "Invalid email or password"
    ACCOUNT_LOCKED = "Account is locked due to multiple failed attempts"
    ACCOUNT_DISABLED = "Account is disabled"
    INVALID_TOKEN = "Invalid or expired token"
    TOKEN_EXPIRED = "Token has expired"
    PASSWORD_TOO_WEAK = "Password does not meet security requirements"
    OLD_PASSWORD_INCORRECT = "Current password is incorrect"
    SESSION_EXPIRED = "Session has expired"

# Validation Constants
class ValidationConstants:
    # Field Requirements
    REQUIRED_FIELD = "This field is required"
    INVALID_EMAIL = "Invalid email format"
    INVALID_PHONE = "Invalid phone number format"
    INVALID_DATE = "Invalid date format"
    INVALID_TIME = "Invalid time format"
    
    # Length Validations
    MIN_PASSWORD_LENGTH = "Password must be at least 8 characters long"
    MAX_NAME_LENGTH = "Name must not exceed 100 characters"
    MAX_DESCRIPTION_LENGTH = "Description must not exceed 500 characters"
    
    # Format Validations
    INVALID_ID_FORMAT = "Invalid ID format"
    INVALID_STATUS = "Invalid status value"
    INVALID_ENUM_VALUE = "Invalid enum value provided"

# Standard Response Templates
class ResponseTemplate:
    @staticmethod
    def success_response(message: str = ResponseMessage.SUCCESS, data: Any = None) -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error_response(message: str, error_code: str = None, details: Any = None) -> Dict[str, Any]:
        response = {
            "success": False,
            "message": message
        }
        if error_code:
            response["error_code"] = error_code
        if details:
            response["details"] = details
        return response
    
    @staticmethod
    def validation_error_response(errors: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": False,
            "message": ResponseMessage.VALIDATION_ERROR,
            "errors": errors
        }

# Error Codes for Different Modules
class ErrorCode:
    # Employee Module
    EMP_001 = "EMP_001"  # Employee not found
    EMP_002 = "EMP_002"  # Employee already exists
    EMP_003 = "EMP_003"  # Invalid employee data
    
    # Attendance Module
    ATT_001 = "ATT_001"  # Already checked in
    ATT_002 = "ATT_002"  # Not checked in
    ATT_003 = "ATT_003"  # Invalid attendance time
    
    # Leave Module
    LEV_001 = "LEV_001"  # Leave not found
    LEV_002 = "LEV_002"  # Insufficient leave balance
    LEV_003 = "LEV_003"  # Overlapping leave dates
    
    # Role Module
    ROL_001 = "ROL_001"  # Role not found
    ROL_002 = "ROL_002"  # Insufficient permissions
    ROL_003 = "ROL_003"  # Role already exists
    
    # Department Module
    DEPT_001 = "DEPT_001"  # Department not found
    DEPT_002 = "DEPT_002"  # Department has employees
    DEPT_003 = "DEPT_003"  # Invalid department head
    
    # Auth Module
    AUTH_001 = "AUTH_001"  # Invalid credentials
    AUTH_002 = "AUTH_002"  # Token expired
    AUTH_003 = "AUTH_003"  # Account locked
    
    # Hierarchy Module
    HIER_001 = "HIER_001"  # Circular hierarchy
    HIER_002 = "HIER_002"  # Invalid manager
    HIER_003 = "HIER_003"  # Self reporting not allowed

# Leave Types
class LeaveType:
    SICK = "sick"
    CASUAL = "casual"
    ANNUAL = "annual"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    EMERGENCY = "emergency"
    UNPAID = "unpaid"

# Leave Status
class LeaveStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# Attendance Status
class AttendanceStatus:
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LATE = "late"
    ON_LEAVE = "on_leave"

# Employee Status
class EmployeeStatus:
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"

# User Roles
class UserRole:
    SUPER_ADMIN = "super_admin"
    HR_ADMIN = "hr_admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    DEPARTMENT_HEAD = "department_head"

# Permissions
class Permission:
    # Employee Management
    VIEW_EMPLOYEES = "view_employees"
    CREATE_EMPLOYEE = "create_employee"
    UPDATE_EMPLOYEE = "update_employee"
    DELETE_EMPLOYEE = "delete_employee"
    
    # Attendance Management
    VIEW_ATTENDANCE = "view_attendance"
    MARK_ATTENDANCE = "mark_attendance"
    UPDATE_ATTENDANCE = "update_attendance"
    VIEW_ALL_ATTENDANCE = "view_all_attendance"
    
    # Leave Management
    APPLY_LEAVE = "apply_leave"
    APPROVE_LEAVE = "approve_leave"
    VIEW_LEAVE = "view_leave"
    VIEW_ALL_LEAVES = "view_all_leaves"
    
    # Department Management
    VIEW_DEPARTMENTS = "view_departments"
    CREATE_DEPARTMENT = "create_department"
    UPDATE_DEPARTMENT = "update_department"
    DELETE_DEPARTMENT = "delete_department"
    
    # Role Management
    VIEW_ROLES = "view_roles"
    CREATE_ROLE = "create_role"
    UPDATE_ROLE = "update_role"
    DELETE_ROLE = "delete_role"
    ASSIGN_ROLE = "assign_role"
    
    # Audit Logs
    VIEW_AUDIT_LOGS = "view_audit_logs"
    VIEW_ACTIVITY_LOGS = "view_activity_logs"

# Database Constants
class DatabaseConstants:
    CONNECTION_ERROR = "Database connection error"
    TRANSACTION_FAILED = "Database transaction failed"
    CONSTRAINT_VIOLATION = "Database constraint violation"
    DUPLICATE_ENTRY = "Duplicate entry in database"

# File Upload Constants
class FileConstants:
    INVALID_FILE_TYPE = "Invalid file type"
    FILE_TOO_LARGE = "File size exceeds maximum limit"
    FILE_UPLOAD_FAILED = "File upload failed"
    FILE_NOT_FOUND = "File not found"
    INVALID_FILE_FORMAT = "Invalid file format"

# API Rate Limiting
class RateLimitConstants:
    RATE_LIMIT_EXCEEDED = "Rate limit exceeded"
    TOO_MANY_REQUESTS = "Too many requests"

# Pagination Constants
class PaginationConstants:
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    INVALID_PAGE_NUMBER = "Invalid page number"
    INVALID_PAGE_SIZE = "Invalid page size"