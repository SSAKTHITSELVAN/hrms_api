from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_data.employee_education_model import Education
from app.employee_management.employee_education.education_schema import (
    EducationCreate, 
    EducationUpdate,
    EducationResponse
)
from app.employee_management.employee_education.education_repository import (
    EmployeeEducationRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status

# Initialize response messages
response_message = ResponseMessage()


class EmployeeEducationService:
    """
    Service layer for employee education operations.
    Handles business logic and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmployeeEducationRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmployeeEducationRepository()
    
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
        """
        return await self.repository.create_employee_education(db, education_data)
    
    async def get_employee_education_by_id(
        self, 
        db: AsyncSession, 
        education_id: str
    ) -> Education:
        """
        Retrieve employee education by ID.
        
        Args:
            db: Database session
            education_id: Unique identifier for education record
            
        Returns:
            Education: Education object
            
        Raises:
            AppException: If education record not found
        """
        education = await self.repository.get_employee_education_by_id(db, education_id)
        
        if not education:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Education record not found with ID: {education_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return education
    
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
        """
        return await self.repository.get_employee_education_by_employee_id(db, employee_id)
    
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
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[Education]: List of education objects
        """
        return await self.repository.get_all_employee_education(db, skip, limit)
    
    async def update_employee_education(
        self, 
        db: AsyncSession, 
        education_id: str,
        update_data: EducationUpdate
    ) -> Education:
        """
        Update employee education record by education ID.
        
        Args:
            db: Database session
            education_id: Unique identifier for education record
            update_data: Data to update
            
        Returns:
            Education: Updated education object
            
        Raises:
            AppException: If education record not found or update fails
        """
        updated_education = await self.repository.update_employee_education(
            db, education_id, update_data
        )
        
        if not updated_education:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Education record not found with ID: {education_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_education
    
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
            bool: True if deletion successful
            
        Raises:
            AppException: If education record not found
        """
        deleted = await self.repository.delete_employee_education(db, education_id)
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Education record not found with ID: {education_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
    async def get_education_count(self, db: AsyncSession) -> int:
        """
        Get total count of education records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_education_count(db)
    
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
        """
        return await self.repository.get_highest_qualifications(db, employee_id)