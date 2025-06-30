from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authentication.auth_employee import Employee
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import List
from app.authentication.authentication_schema import EmployeeCreate
from app.core.utilities.exceptions.base import AppException
from app.core.constants import AuthConstants

# Authentication Constants
authentication_constants = AuthConstants()


class AuthEmployeeRepositoy:
    """
    Repository for handling employee authentication operations.
    """
    
    async def list_employees_repository(self, db: AsyncSession) -> List[Employee]:
        '''
        Return all the employees
        '''
        try:
            query = select(Employee)
            result = await db.execute(query)
            
            employees = result.scalars().all()
            return employees
        except SQLAlchemyError as e:
            raise HTTPException(
                                    status_code=409,
                                    detail=f"Database query failed while fetching companies: {e}"
                                )
        except Exception as e:
            raise HTTPException(
                                    status_code=409,
                                    detail=f"Unexpected error in CompanyRepository: {str(e)}"
                                )
    
    
    async def create_employee_repository(self, db: AsyncSession, employee_data: EmployeeCreate) -> Employee:
        '''
        Create new employee
        '''
        
        try:
            query = select(Employee).where(Employee.employee_code == employee_data.employee_code)
            result = await db.execute(query)
            existing_company = result.scalar_one_or_none()
            
            if existing_company:
                raise AppException(
                    message_key=authentication_constants.INVALID_CREDENTIALS,
                    details= f"Employee with the code {employee_data.employee_code} does not exists.",
                    status_code=409
                )
            
            
            new_employee = Employee(**employee_data.dict())
            
            db.add(new_employee)
            await db.commit()
            await db.refresh(new_employee)
            return new_employee
        
        except SQLAlchemyError as e:
            await db.rollback()  # 🔁 Ensure rollback on any DB-level error
            raise AppException(
                message_key="DB_ERROR",
                details=str(e),
                status_code=500
            )