from typing import List, Optional
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_work_experience_model import WorkExperience
from app.employee_management.employee_work_experience.work_experience_schema import (
    WorkExperienceCreate, 
    WorkExperienceUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmployeeWorkExperienceRepository:
    """
    Repository class for handling all database operations related to employee work experience.
    Implements full CRUD operations with proper error handling and validation.
    """

    async def create_employee_work_experience(
        self, 
        db: AsyncSession, 
        work_experience_data: WorkExperienceCreate
    ) -> WorkExperience:
        """
        Create new employee work experience record.
        
        Args:
            db: Database session
            work_experience_data: Work experience data to create
            
        Returns:
            WorkExperience: Created work experience object
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Create new work experience
            new_work_experience = WorkExperience(**work_experience_data.model_dump())
            db.add(new_work_experience)
            await db.commit()
            await db.refresh(new_work_experience)
            
            return new_work_experience
            
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

    async def get_employee_work_experience_by_id(
        self, 
        db: AsyncSession, 
        experience_id: str
    ) -> Optional[WorkExperience]:
        """
        Retrieve employee work experience by experience ID.
        
        Args:
            db: Database session
            experience_id: Unique identifier for work experience
            
        Returns:
            WorkExperience or None: Work experience object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(WorkExperience).where(
                WorkExperience.experience_id == experience_id
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve work experience: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_employee_work_experiences_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[WorkExperience]:
        """
        Retrieve all work experiences for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            List[WorkExperience]: List of work experience objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(WorkExperience).where(
                WorkExperience.employee_id == employee_id
            ).order_by(WorkExperience.start_date.desc())
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve work experiences for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_employee_work_experiences(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkExperience]:
        """
        Retrieve all employee work experiences with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[WorkExperience]: List of work experience objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(WorkExperience).offset(skip).limit(limit).order_by(
                WorkExperience.start_date.desc()
            )
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve work experiences list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_work_experience(
        self, 
        db: AsyncSession, 
        experience_id: str,
        update_data: WorkExperienceUpdate
    ) -> Optional[WorkExperience]:
        """
        Update employee work experience.
        
        Args:
            db: Database session
            experience_id: Unique identifier for work experience
            update_data: Data to update
            
        Returns:
            WorkExperience or None: Updated work experience object
            
        Raises:
            AppException: If work experience not found or database error occurs
        """
        try:
            # Check if work experience exists
            existing_experience = await self.get_employee_work_experience_by_id(
                db, experience_id
            )
            
            if not existing_experience:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Work experience not found with ID: {experience_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_experience
            
            # Perform update
            query = (
                update(WorkExperience)
                .where(WorkExperience.experience_id == experience_id)
                .values(**update_dict)
                .returning(WorkExperience)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_experience = result.scalar_one_or_none()
            if updated_experience:
                await db.refresh(updated_experience)
            
            return updated_experience
            
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
                details=f"Failed to update work experience: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_employee_work_experience(
        self, 
        db: AsyncSession, 
        experience_id: str
    ) -> bool:
        """
        Delete employee work experience.
        
        Args:
            db: Database session
            experience_id: Unique identifier for work experience
            
        Returns:
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if work experience exists
            existing_experience = await self.get_employee_work_experience_by_id(
                db, experience_id
            )
            
            if not existing_experience:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Work experience not found with ID: {experience_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete work experience
            query = delete(WorkExperience).where(
                WorkExperience.experience_id == experience_id
            )
            
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete work experience: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def search_work_experiences(
        self, 
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkExperience]:
        """
        Search employee work experiences by company name, job title, or location.
        
        Args:
            db: Database session
            search_term: Term to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[WorkExperience]: List of matching work experiences
            
        Raises:
            AppException: If database error occurs
        """
        try:
            search_pattern = f"%{search_term.lower()}%"
            
            query = select(WorkExperience).where(
                (WorkExperience.company_name.ilike(search_pattern)) |
                (WorkExperience.job_title.ilike(search_pattern)) |
                (WorkExperience.location.ilike(search_pattern))
            ).offset(skip).limit(limit).order_by(WorkExperience.start_date.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Search operation failed: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_current_work_experiences(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkExperience]:
        """
        Get all current work experiences (where end_date is null).
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[WorkExperience]: List of current work experiences
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(WorkExperience).where(
                WorkExperience.end_date.is_(None)
            ).offset(skip).limit(limit).order_by(WorkExperience.start_date.desc())
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve current work experiences: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_work_experience_count(self, db: AsyncSession) -> int:
        """
        Get total count of work experience records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(func.count(WorkExperience.experience_id))
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_work_experience_count_by_employee(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> int:
        """
        Get count of work experience records for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            int: Count of records for the employee
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(func.count(WorkExperience.experience_id)).where(
                WorkExperience.employee_id == employee_id
            )
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get employee work experience count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )