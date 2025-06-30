from app.authentication.authentication_repository import AuthEmployeeRepositoy
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authentication.auth_employee import Employee
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.authentication.authentication_schema import EmployeeCreate
from app.core.security import hash_password

#####################################
### Auto update Role id for employee
#####################################

from app.department.department_repository import DepartmentRepository


class AuthEmployeeSerive:
    """
    Service layer for authentication-related operations.
    Handles business logic and orchestrates repository operations.
    """
    
    def __init__(self, repository: AuthEmployeeRepositoy = None) -> None:
        self.repository = repository or AuthEmployeeRepositoy()
    
    async def list_employees_service(self, db: AsyncSession) -> List[Employee]:
        try:
            companies = await self.repository.list_employees_repository(db)
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
    
    
    async def create_employee_service(self, db: AsyncSession, employee_create: EmployeeCreate) -> Employee:
        
        plain_password = employee_create.employee_hashed_password
        department_id = employee_create.employee_department_id
        employee_create.employee_hashed_password = hash_password(plain_password)
        
        #######################################
        ####### Auto role id update
        ########################################
        department_repository = DepartmentRepository()
        targeted_department = await department_repository.get_department_repository(db, department_id)
        employee_create.employee_role_id = targeted_department.default_employee_role_id
        
        created_employee = await self.repository.create_employee_repository(db, employee_create)
        return created_employee