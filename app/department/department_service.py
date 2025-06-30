from app.department.department_repository import DepartmentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.organization.department_model import Department
from app.department.department_schema import DepartmentCreate, DepartmentUpdate
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select, func
from app.models.authentication.auth_employee import Employee

#####################################################
### Auto Employee creation based on head count
#####################################################
from app.authentication.authentication_schema import EmployeeCreate, EmployeeStatus
from app.authentication.authentication_service import AuthEmployeeSerive
from app.tasks.auto_employee_generator import employee_code_generator, employee_password_generator


class DepartmentService:

    def __init__(self, repository: DepartmentRepository = None) -> None:
        self.repository = repository or DepartmentRepository()

    async def list_departments_service(self, db: AsyncSession) -> List[Department]:
        try:
            departments = await self.repository.list_departments_repository(db)
            return departments
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service failed to retrieve departments from the database: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service unexpected error while listing departments: {str(e)}"
            )

    async def get_department_service(self, db: AsyncSession, department_id: str) -> Department:
        try:
            department = await self.repository.get_department_repository(db, department_id)
            return department
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service failed to retrieve department from the database: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service unexpected error while retrieving department: {str(e)}"
            )

    async def create_department_service(self, db: AsyncSession, department_create: DepartmentCreate) -> Department:
        try:
            created_department = await self.repository.create_department_repository(db, department_create)
                
            #####################################################
            ### Auto Employee creation based on head count
            #####################################################
            auth_employee_service = AuthEmployeeSerive()
            
            company_id = created_department.company_id
            company_code = "EMP"
            department_id = created_department.department_id
            department_code = created_department.department_code
            head_count = created_department.department_employee_count
            
            # ✅ Query existing employees count for this department
            result = await db.execute(
                select(func.count()).select_from(Employee).where(Employee.employee_department_id == department_id)
            )
            existing_count = result.scalar()  # gives integer
            
            print(f"Already existing {existing_count} employees for department {department_code}")

            # ✅ Start from existing_count + 1
            for i in range(1, head_count + 1):
                actual_count = existing_count + i
                employee_code = employee_code_generator(company_code, department_code, actual_count)
                plain_password = employee_password_generator(company_code, department_code, actual_count)
                default_employee = default_employee_creation(company_id, department_id, employee_code, plain_password)
                await auth_employee_service.create_employee_service(db, default_employee)
                print(f"Employee {employee_code} is created successfully")

            return created_department
        
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while creating department: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentService: {str(e)}"
            )

    async def update_department_service(self, db: AsyncSession, department_update: DepartmentUpdate, department_id: str) -> Department:
        try:
            updated_department = await self.repository.update_department_repository(db, department_update, department_id)
            return updated_department
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while updating department: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentService: {str(e)}"
            )

    async def delete_department_service(self, db: AsyncSession, department_id: str) -> str:
        try:
            delete_department_message = await self.repository.delete_department_repository(db, department_id)
            return delete_department_message
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while deleting department: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentService: {str(e)}"
            )


#####################################
#### Default employee
#####################################

def default_employee_creation(
    company_id: str,
    department_id: str,
    employee_code: str,
    plain_password: str,
) -> EmployeeCreate:
    
    return EmployeeCreate(
        company_id=company_id,
        employee_code=employee_code,
        employee_department_id=department_id,
        employee_hashed_password=plain_password,
        employee_status=EmployeeStatus.ACTIVE
    )

