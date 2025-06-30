from app.models.organization.department_model import Department
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.department.department_schema import DepartmentCreate, DepartmentUpdate
from fastapi import HTTPException, status
from typing import List

class DepartmentRepository:
    """
    Repository for handling department data operations.
    """

    async def list_departments_repository(self, db: AsyncSession) -> List[Department]:
        """
        Retrieve all available departments from the database.
        """
        try:
            query = select(Department)
            result = await db.execute(query)
            departments = result.scalars().all()
            return departments
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=409,
                detail=f"Database query failed while fetching departments: {e}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=409,
                detail=f"Unexpected error in DepartmentRepository: {str(e)}"
            )

    async def get_department_repository(self, db: AsyncSession, department_id: str) -> Department:
        """
        Retrieve a department by ID.
        """
        try:
            query = select(Department).where(Department.department_id == department_id)
            result = await db.execute(query)
            department = result.scalar_one_or_none()

            if not department:
                raise HTTPException(
                    status_code=409,
                    detail=f"Department with id '{department_id}' does not exist."
                )

            return department

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=409,
                detail=f"Database query failed while fetching department: {e}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=409,
                detail=f"Unexpected error in DepartmentRepository: {str(e)}"
            )

    async def create_department_repository(self, db: AsyncSession, department_data: DepartmentCreate) -> Department:
        """
        Create a new department after checking uniqueness of department_code.
        """
        try:
            # Check if department_code already exists
            query = select(Department).where((Department.department_code == department_data.department_code) & (Department.company_id == department_data.company_id))
            result = await db.execute(query)
            existing_department = result.scalar_one_or_none()

            if existing_department:
                raise HTTPException(
                    status_code=409,
                    detail=f"Department with code '{department_data.department_code}' already exists."
                )

            # Create the Department model instance from schema
            new_department = Department(**department_data.dict())

            db.add(new_department)
            await db.commit()
            await db.refresh(new_department)
            return new_department

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while creating department: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentRepository: {str(e)}"
            )

    async def update_department_repository(self, db: AsyncSession, department_data: DepartmentUpdate, department_id: str) -> Department:
        """
        Update an existing department.
        """
        try:
            query = select(Department).where(Department.department_id == department_id)
            result = await db.execute(query)
            existing_department = result.scalar_one_or_none()

            if not existing_department:
                raise HTTPException(
                    status_code=409,
                    detail=f"Department with id '{department_id}' does not exist."
                )

            update_data = department_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_department, key, value)

            await db.commit()
            await db.refresh(existing_department)
            return existing_department

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while updating department: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentRepository: {str(e)}"
            )

    async def delete_department_repository(self, db: AsyncSession, department_id: str) -> str:
        """
        Delete an existing department.
        """
        try:
            query = select(Department).where(Department.department_id == department_id)
            result = await db.execute(query)
            existing_department = result.scalar_one_or_none()

            if not existing_department:
                raise HTTPException(
                    status_code=409,
                    detail=f"Department with id '{department_id}' does not exist."
                )

            await db.delete(existing_department)
            await db.commit()
            return f"Department '{department_id}' deleted successfully."

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while deleting department: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in DepartmentRepository: {str(e)}"
            )
