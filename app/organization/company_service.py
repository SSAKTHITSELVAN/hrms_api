# from app.repositories.organization.company_repository import CompanyRepository
# from app.repositories.organization.department_repository import DepartmentRepository
# from app.repositories.organization.role_repository import RoleRepository
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import SQLAlchemyError
# from app.models.organization.company_model import Company
# from app.schemas.organization.company_schema import CompanyCreate, CompanyUpdate
# from app.schemas.organization.department_schema import DepartmentCreate, DepartmentType, DepartmentStatus, ConfidentialityLevel
# from app.schemas.organization.role_schema import RoleCreate
# from fastapi import HTTPException, status
# from typing import List

# class CompanyService:
    
#     def __init__(self, repository: CompanyRepository = None) -> None:
#         self.repository = repository or CompanyRepository()
    
#     async def list_companies_service(self, db: AsyncSession)-> List[Company]:
#         try:
#             companies = await self.repository.list_companies_repository(db)
#             return companies
#         except SQLAlchemyError as e:
#             # Optionally log the error here
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service failed to retrieve companies from the database.: {str(e)}"
#             )
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service unexpected error while listing companies: {str(e)}"
#             )
    
#     async def get_company_service(self, db: AsyncSession, company_id: str) -> Company:
#         try:
#             company = await self.repository.get_company_repository(db, company_id)
#             return company
#         except SQLAlchemyError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service failed to retrieve company from the database.: {str(e)}"
#             )
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service unexpected error while listing companies: {str(e)}"
#             )
        
#     async def create_company_service(self, db: AsyncSession, company_create: CompanyCreate) -> Company:
#         try:
#             created_company = await self.repository.create_company_repository(db, company_create)
#             # return created_company
#             department_repository = DepartmentRepository()
#             role_repository = RoleRepository()
#             ####### Defaults ################

            
            
#             admin_role = RoleCreate(
#                 company_id=created_company.company_id,
#                 role_name="Admin Role",
#                 role_code="ADMIN001",
#                 role_description="Full Access Administrative Role",
#                 is_system_role=True,
#                 is_active=True,

#                 # ✅ Set all permissions to True
#                 can_create_employee=True,
#                 can_view_all_employees=True,
#                 can_view_own_profile=True,
#                 can_view_team_members=True,
#                 can_view_department_employees=True,
#                 can_edit_all_employee_profiles=True,
#                 can_edit_own_profile=True,
#                 can_edit_team_profiles=True,
#                 can_delete_employee=True,
#                 can_archive_employee=True,
#                 can_restore_employee=True,
#                 can_activate_employee=True,
#                 can_deactivate_employee=True,
#                 can_suspend_employee=True,
#                 can_view_employee_documents=True,
#                 can_upload_employee_documents=True,
#                 can_delete_employee_documents=True,

#                 can_checkin_own=True,
#                 can_checkout_own=True,
#                 can_start_break_own=True,
#                 can_end_break_own=True,
#                 can_view_own_attendance=True,
#                 can_view_team_attendance=True,
#                 can_view_department_attendance=True,
#                 can_view_all_attendance=True,
#                 can_edit_own_attendance=True,
#                 can_edit_team_attendance=True,
#                 can_edit_all_attendance=True,
#                 can_delete_attendance=True,
#                 can_approve_attendance=True,
#                 can_reject_attendance=True,

#                 can_apply_own_leave=True,
#                 can_apply_leave_behalf=True,
#                 can_cancel_own_leave=True,
#                 can_cancel_team_leave=True,
#                 can_view_own_leave=True,
#                 can_view_team_leave=True,
#                 can_view_department_leave=True,
#                 can_view_all_leave=True,
#                 can_approve_team_leave=True,
#                 can_approve_department_leave=True,
#                 can_approve_all_leave=True,
#                 can_reject_team_leave=True,
#                 can_reject_department_leave=True,
#                 can_reject_all_leave=True,
#                 can_edit_own_leave=True,
#                 can_edit_team_leave=True,
#                 can_edit_all_leave=True,
#                 can_delete_leave_records=True,
#                 can_create_leave_types=True,
#                 can_edit_leave_types=True,
#                 can_delete_leave_types=True,
#                 can_manage_leave_policies=True,
#                 can_view_all_leave_balances=True,

#                 can_create_department=True,
#                 can_view_all_departments=True,
#                 can_view_own_department=True,
#                 can_edit_all_departments=True,
#                 can_edit_own_department=True,
#                 can_delete_department=True,
#                 can_assign_employees_department=True,
#                 can_remove_employees_department=True,
#                 can_transfer_employees=True,
#                 can_manage_department_hierarchy=True,
#                 can_assign_department_head=True,

#                 can_create_roles=True,
#                 can_view_all_roles=True,
#                 can_edit_all_roles=True,
#                 can_delete_roles=True,
#                 can_assign_roles=True,
#                 can_unassign_roles=True,

#                 can_view_company_details=True,
#                 can_edit_company_details=True,
#                 can_manage_company_settings=True,
#                 can_view_org_hierarchy=True,
#                 can_manage_org_hierarchy=True,

#                 can_generate_employee_reports=True,
#                 can_generate_attendance_reports=True,
#                 can_generate_leave_reports=True,
#                 can_generate_department_reports=True,
#                 can_create_custom_reports=True,

#                 can_export_employee_data=True,
#                 can_export_attendance_data=True,
#                 can_export_leave_data=True,
#                 can_export_all_data=True,

#                 can_view_employee_dashboard=True,
#                 can_view_attendance_dashboard=True,
#                 can_view_leave_dashboard=True,
#                 can_view_executive_dashboard=True,

#                 can_view_all_audit_logs=True,
#                 can_view_own_audit_logs=True,
#                 can_view_team_audit_logs=True,
#                 can_export_audit_logs=True,
#                 can_manage_system_settings=True,
#                 can_create_system_backup=True,
#                 can_restore_system_backup=True,
#                 can_enable_maintenance_mode=True,
#                 can_create_user_accounts=True,
#                 can_edit_user_accounts=True,
#                 can_delete_user_accounts=True,
#                 can_reset_user_passwords=True,
#                 can_lock_user_accounts=True,
#                 can_unlock_user_accounts=True,
#                 )
            
            
#             role_created = await role_repository.create_role_repository(db, admin_role)
            
#             admin_department = DepartmentCreate(
#                 company_id=created_company.company_id,
#                 department_code="ADMIN001",
#                 department_name="Administrative Department",
#                 department_description="This is the default Administrative department",
                
#                 department_employee_count=1,
#                 max_employee_capacity=10,
#                 department_type=DepartmentType.ADMINISTRATIVE,
                
#                 break_duration_minutes=60,
#                 flexible_hours_allowed=False,
#                 remote_work_allowed=False,
#                 overtime_allowed=True,
#                 weekend_work_required=False,

#                 auto_approve_leave_days=0,
#                 max_consecutive_leave_days=30,
#                 advance_leave_notice_days=7,

#                 late_arrival_grace_minutes=15,
#                 early_departure_requires_approval=True,
                
#                 default_employee_role_id=role_created.role_id,
                
#                 can_employees_view_others=False,
#                 can_employees_request_overtime=True,

#                 show_department_calendar=True,
#                 show_department_announcements=True,
#                 show_team_directory=True,
#                 allow_profile_updates=True,

#                 track_login_activity=True,
#                 track_attendance_changes=True,
#                 track_leave_activities=True,
#                 track_profile_changes=True,
#                 audit_retention_days=365,

#                 department_status=DepartmentStatus.ACTIVE,
#                 last_restructure_date=None,

#                 is_billable_department=False,
#                 requires_timesheet=False,
#                 project_based_work=False,
#                 client_facing=False,

#                 requires_background_check=False,
#                 confidentiality_level=ConfidentialityLevel.STANDARD
#                 )
            
#             department_created = await department_repository.create_department_repository(db, admin_department)
            
#             return created_company
            
#         except SQLAlchemyError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service error while creating company: {str(e)}"
#             )
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Unexpected error in CompanyService: {str(e)}"
#             )
    
#     async def update_company_service(self, db: AsyncSession, company_update: CompanyUpdate, company_id: str) -> Company:
#         try:
#             created_company = await self.repository.update_company_repository(db, company_update, company_id)
#             return created_company
#         except SQLAlchemyError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service error while updating company: {str(e)}"
#             )
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Unexpected error in CompanyService: {str(e)}"
#             )
    
#     async def delete_company_service(self, db: AsyncSession, company_id: str) -> str:
#         try:
#             delete_company_message = await self.repository.delete_company_repository(db, company_id)
#             return delete_company_message
#         except SQLAlchemyError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Service error while deleting company: {str(e)}"
#             )
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail= f"Unexpected error in CompanyService: {str(e)}"
#             )






from app.organization.company_repository import CompanyRepository
from app.department.department_repository import DepartmentRepository
from app.department.department_service import DepartmentService
from app.role.role_repository import RoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.organization.company_model import Company
from app.organization.company_schema import CompanyCreate, CompanyUpdate
from app.department.department_schema import DepartmentCreate, DepartmentType, DepartmentStatus, ConfidentialityLevel
from app.role.role_schema import RoleCreate
from fastapi import HTTPException, status
from typing import List


class CompanyService:
    """
    Service layer for company-related operations.
    Handles business logic and orchestrates repository operations.
    """
    
    def __init__(self, repository: CompanyRepository = None) -> None:
        self.repository = repository or CompanyRepository()
    
    # ========================================
    # COMPANY LISTING AND RETRIEVAL METHODS
    # ========================================
    
    async def list_companies_service(self, db: AsyncSession) -> List[Company]:
        """
        Retrieve all companies from the database.
        
        Args:
            db: Database session
            
        Returns:
            List[Company]: List of all companies
            
        Raises:
            HTTPException: If database operation fails
        """
        try:
            companies = await self.repository.list_companies_repository(db)
            return companies
            
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[CompanyService.list_companies_service] Database error while retrieving companies: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"[CompanyService.list_companies_service] Unexpected error while listing companies: {str(e)}"
            )
    
    async def get_company_service(self, db: AsyncSession, company_id: str) -> Company:
        """
        Retrieve a specific company by ID.
        
        Args:
            db: Database session
            company_id: Unique identifier for the company
            
        Returns:
            Company: The requested company object
            
        Raises:
            HTTPException: If company not found or database operation fails
        """
        company = await self.repository.get_company_repository(db, company_id)
        return company
    
    # ========================================
    # COMPANY CREATION METHOD
    # ========================================
    
    async def create_company_service(self, db: AsyncSession, company_create: CompanyCreate) -> Company:
        """
        Create a new company with default administrative role and department.
        
        This method performs the following operations:
        1. Creates the company
        2. Creates a default admin role with full permissions
        3. Creates a default administrative department
        
        Args:
            db: Database session
            company_create: Company creation data
            
        Returns:
            Company: The newly created company
            
        Raises:
            HTTPException: If any step in the creation process fails
        """
        
        # Step 1: Create the company
        created_company = await self.repository.create_company_repository(db, company_create)
        
        
        # Initialize repositories for default setup
        department_repository = DepartmentService()
        role_repository = RoleRepository()
        
        # Step 2: Create default admin role
        admin_role = self._create_default_admin_role(created_company.company_id)
        role_created = await role_repository.create_role_repository(db, admin_role)
        
        # Step 3: Create default administrative department
        admin_department = self._create_default_admin_department(
            created_company.company_id, 
            role_created.role_id
            )
        department_created = await department_repository.create_department_service(db, admin_department)
        
        return created_company
    
    
    
    # ========================================
    # COMPANY UPDATE AND DELETE METHODS
    # ========================================
    
    async def update_company_service(self, db: AsyncSession, company_update: CompanyUpdate, company_id: str) -> Company:
        """
        Update an existing company.
        
        Args:
            db: Database session
            company_update: Updated company data
            company_id: ID of the company to update
            
        Returns:
            Company: The updated company object
            
        Raises:
            HTTPException: If update operation fails
        """
        try:
            updated_company = await self.repository.update_company_repository(db, company_update, company_id)
            return updated_company
            
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[CompanyService.update_company_service] Database error while updating company {company_id}: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"[CompanyService.update_company_service] Unexpected error while updating company {company_id}: {str(e)}"
            )
    
    async def delete_company_service(self, db: AsyncSession, company_id: str) -> str:
        """
        Delete a company from the database.
        
        Args:
            db: Database session
            company_id: ID of the company to delete
            
        Returns:
            str: Deletion confirmation message
            
        Raises:
            HTTPException: If deletion operation fails
        """
        try:
            delete_message = await self.repository.delete_company_repository(db, company_id)
            return delete_message
            
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[CompanyService.delete_company_service] Database error while deleting company {company_id}: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"[CompanyService.delete_company_service] Unexpected error while deleting company {company_id}: {str(e)}"
            )
    
    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================
    
    def _create_default_admin_role(self, company_id: str) -> RoleCreate:
        """
        Create default admin role configuration with full permissions.
        
        Args:
            company_id: ID of the company this role belongs to
            
        Returns:
            RoleCreate: Admin role configuration object
        """
        return RoleCreate(
            company_id=company_id,
            role_name="Admin Role",
            role_code="ADMIN001",
            role_description="Full Access Administrative Role",
            is_system_role=True,
            is_active=True,

            # Employee Management Permissions
            can_create_employee=True,
            can_view_all_employees=True,
            can_view_own_profile=True,
            can_view_team_members=True,
            can_view_department_employees=True,
            can_edit_all_employee_profiles=True,
            can_edit_own_profile=True,
            can_edit_team_profiles=True,
            can_delete_employee=True,
            can_archive_employee=True,
            can_restore_employee=True,
            can_activate_employee=True,
            can_deactivate_employee=True,
            can_suspend_employee=True,
            can_view_employee_documents=True,
            can_upload_employee_documents=True,
            can_delete_employee_documents=True,

            # Attendance Management Permissions
            can_checkin_own=True,
            can_checkout_own=True,
            can_start_break_own=True,
            can_end_break_own=True,
            can_view_own_attendance=True,
            can_view_team_attendance=True,
            can_view_department_attendance=True,
            can_view_all_attendance=True,
            can_edit_own_attendance=True,
            can_edit_team_attendance=True,
            can_edit_all_attendance=True,
            can_delete_attendance=True,
            can_approve_attendance=True,
            can_reject_attendance=True,

            # Leave Management Permissions
            can_apply_own_leave=True,
            can_apply_leave_behalf=True,
            can_cancel_own_leave=True,
            can_cancel_team_leave=True,
            can_view_own_leave=True,
            can_view_team_leave=True,
            can_view_department_leave=True,
            can_view_all_leave=True,
            can_approve_team_leave=True,
            can_approve_department_leave=True,
            can_approve_all_leave=True,
            can_reject_team_leave=True,
            can_reject_department_leave=True,
            can_reject_all_leave=True,
            can_edit_own_leave=True,
            can_edit_team_leave=True,
            can_edit_all_leave=True,
            can_delete_leave_records=True,
            can_create_leave_types=True,
            can_edit_leave_types=True,
            can_delete_leave_types=True,
            can_manage_leave_policies=True,
            can_view_all_leave_balances=True,

            # Department Management Permissions
            can_create_department=True,
            can_view_all_departments=True,
            can_view_own_department=True,
            can_edit_all_departments=True,
            can_edit_own_department=True,
            can_delete_department=True,
            can_assign_employees_department=True,
            can_remove_employees_department=True,
            can_transfer_employees=True,
            can_manage_department_hierarchy=True,
            can_assign_department_head=True,

            # Role Management Permissions
            can_create_roles=True,
            can_view_all_roles=True,
            can_edit_all_roles=True,
            can_delete_roles=True,
            can_assign_roles=True,
            can_unassign_roles=True,

            # Company Management Permissions
            can_view_company_details=True,
            can_edit_company_details=True,
            can_manage_company_settings=True,
            can_view_org_hierarchy=True,
            can_manage_org_hierarchy=True,

            # Reporting Permissions
            can_generate_employee_reports=True,
            can_generate_attendance_reports=True,
            can_generate_leave_reports=True,
            can_generate_department_reports=True,
            can_create_custom_reports=True,

            # Data Export Permissions
            can_export_employee_data=True,
            can_export_attendance_data=True,
            can_export_leave_data=True,
            can_export_all_data=True,

            # Dashboard Permissions
            can_view_employee_dashboard=True,
            can_view_attendance_dashboard=True,
            can_view_leave_dashboard=True,
            can_view_executive_dashboard=True,

            # System Administration Permissions
            can_view_all_audit_logs=True,
            can_view_own_audit_logs=True,
            can_view_team_audit_logs=True,
            can_export_audit_logs=True,
            can_manage_system_settings=True,
            can_create_system_backup=True,
            can_restore_system_backup=True,
            can_enable_maintenance_mode=True,
            can_create_user_accounts=True,
            can_edit_user_accounts=True,
            can_delete_user_accounts=True,
            can_reset_user_passwords=True,
            can_lock_user_accounts=True,
            can_unlock_user_accounts=True,
        )
    
    def _create_default_admin_department(self, company_id: str, default_role_id: str) -> DepartmentCreate:
        """
        Create default administrative department configuration.
        
        Args:
            company_id: ID of the company this department belongs to
            default_role_id: ID of the default role for this department
            
        Returns:
            DepartmentCreate: Administrative department configuration object
        """
        return DepartmentCreate(
            company_id=company_id,
            department_code="ADMIN001",
            department_name="Administrative Department",
            department_description="This is the default Administrative department",
            
            # Department Capacity Settings
            department_employee_count=1,
            max_employee_capacity=10,
            department_type=DepartmentType.ADMINISTRATIVE,
            
            # Work Schedule Settings
            break_duration_minutes=60,
            flexible_hours_allowed=False,
            remote_work_allowed=False,
            overtime_allowed=True,
            weekend_work_required=False,

            # Leave Policy Settings
            auto_approve_leave_days=0,
            max_consecutive_leave_days=30,
            advance_leave_notice_days=7,

            # Attendance Policy Settings
            late_arrival_grace_minutes=15,
            early_departure_requires_approval=True,
            
            # Default Role Assignment
            default_employee_role_id=default_role_id,
            
            # Employee Interaction Settings
            can_employees_view_others=False,
            can_employees_request_overtime=True,

            # UI/UX Settings
            show_department_calendar=True,
            show_department_announcements=True,
            show_team_directory=True,
            allow_profile_updates=True,

            # Audit and Tracking Settings
            track_login_activity=True,
            track_attendance_changes=True,
            track_leave_activities=True,
            track_profile_changes=True,
            audit_retention_days=365,

            # Department Status
            department_status=DepartmentStatus.ACTIVE,
            last_restructure_date=None,

            # Project and Billing Settings
            is_billable_department=False,
            requires_timesheet=False,
            project_based_work=False,
            client_facing=False,

            # Security Settings
            requires_background_check=False,
            confidentiality_level=ConfidentialityLevel.STANDARD
        )