from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_education_model import Education
from app.employee_management.employee_education.education_schema import (
    EducationCreate, 
    EducationUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmployeeEducationRepository:
    """
    Repository class for handling all database operations related to employee education.
    Implements full CRUD operations with proper error handling.
    """

    async def create_employee_education(
        self, 
        db: AsyncSession, 
        education_data: EducationCreate
    ) -> Education:
        """
        Create new employee education record.
        
        Args:
            db: Database session
            education_data: Education data to create
            
        Returns:
            Education: Created education object
            
        Raises:
            AppException: If database error occurs
        """
        try:
            new_education = Education(**education_data.model_dump())
            db.add(new_education)
            await db.commit()
            await db.refresh(new_education)
            
            return new_education
            
        except IntegrityError as e:
            await db.rollback()
            raise AppException(
                message_key="INTEGRITY_ERROR",
                details=f"Database integrity constraint violated: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Database operation failed: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_employee_education_by_id(
        self, 
        db: AsyncSession, 
        education_id: str
    ) -> Optional[Education]:
        """
        Retrieve employee education by education ID.
        
        Args:
            db: Database session
            education_id: Unique identifier for education record
            
        Returns:
            Education or None: Education object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Education).where(Education.education_id == education_id)
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve education: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_employee_education_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[Education]:
        """
        Retrieve all employee education records by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            List[Education]: List of education objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Education).where(Education.employee_id == employee_id)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve education records for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_employee_education(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Education]:
        """
        Retrieve all employee education records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Education]: List of education objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Education).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve education records list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_education(
        self, 
        db: AsyncSession, 
        education_id: str,
        update_data: EducationUpdate
    ) -> Optional[Education]:
        """
        Update employee education record.
        
        Args:
            db: Database session
            education_id: Unique identifier for education record
            update_data: Data to update
            
        Returns:
            Education or None: Updated education object
            
        Raises:
            AppException: If education not found or database error occurs
        """
        try:
            # Check if education record exists
            existing_education = await self.get_employee_education_by_id(db, education_id)
            
            if not existing_education:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Education record not found with ID: {education_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_education
            
            # Perform update
            query = (
                update(Education)
                .where(Education.education_id == education_id)
                .values(**update_dict)
                .returning(Education)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_education = result.scalar_one_or_none()
            if updated_education:
                await db.refresh(updated_education)
            
            return updated_education
            
        except IntegrityError as e:
            await db.rollback()
            raise AppException(
                message_key="INTEGRITY_ERROR",
                details=f"Database integrity constraint violated: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to update education record: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_employee_education(
        self, 
        db: AsyncSession, 
        education_id: str
    ) -> bool:
        """
        Delete employee education record.
        
        Args:
            db: Database session
            education_id: Unique identifier for education record
            
        Returns:
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if education record exists
            existing_education = await self.get_employee_education_by_id(db, education_id)
            
            if not existing_education:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Education record not found with ID: {education_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete education record
            query = delete(Education).where(Education.education_id == education_id)
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete education record: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_education_count(self, db: AsyncSession) -> int:
        """
        Get total count of education records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(Education.education_id))
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_highest_qualifications(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[Education]:
        """
        Get education records marked as highest qualification for an employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            List[Education]: List of highest qualification records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Education).where(
                and_(
                    Education.employee_id == employee_id,
                    Education.is_highest_qualification == True
                )
            )
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve highest qualifications: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )