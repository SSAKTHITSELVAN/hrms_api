from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models.employee_data.employee_work_experience_model import WorkExperience
from app.employee_management.employee_work_experience.work_experience_schema import (
    WorkExperienceCreate, 
    WorkExperienceUpdate,
    WorkExperienceResponse
)
from app.employee_management.employee_work_experience.work_experience_repository import (
    EmployeeWorkExperienceRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status
import re

# Initialize response messages
response_message = ResponseMessage()


class EmployeeWorkExperienceService:
    """
    Service layer for employee work experience operations.
    Handles business logic, validation, and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmployeeWorkExperienceRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmployeeWorkExperienceRepository()
    
    async def create_employee_work_experience(
        self, 
        db: AsyncSession, 
        work_experience_data: WorkExperienceCreate
    ) -> WorkExperience:
        """
        Create new employee work experience with business logic validation.
        
        Args:
            db: Database session
            work_experience_data: Work experience data to create
            
        Returns:
            WorkExperience: Created work experience object
            
        Raises:
            AppException: If validation fails or creation fails
        """
        # Validate required fields
        self._validate_work_experience_data_create(work_experience_data)
        
        # Validate business rules
        await self._validate_employee_exists(db, work_experience_data.employee_id)
        
        # Create work experience
        created_experience = await self.repository.create_employee_work_experience(
            db, work_experience_data
        )
        
        return created_experience
    
    async def get_employee_work_experience_by_id(
        self, 
        db: AsyncSession, 
        experience_id: str
    ) -> WorkExperience:
        """
        Retrieve employee work experience by ID.
        
        Args:
            db: Database session
            experience_id: Unique identifier for work experience
            
        Returns:
            WorkExperience: Work experience object
            
        Raises:
            AppException: If work experience not found
        """
        work_experience = await self.repository.get_employee_work_experience_by_id(
            db, experience_id
        )
        
        if not work_experience:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Work experience not found with ID: {experience_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return work_experience
    
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
        work_experiences = await self.repository.get_employee_work_experiences_by_employee_id(
            db, employee_id
        )
        
        return work_experiences
    
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
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[WorkExperience]: List of work experience objects
            
        Raises:
            AppException: If validation fails
        """
        # Validate pagination parameters
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.get_all_employee_work_experiences(db, skip, limit)
    
    async def update_employee_work_experience(
        self, 
        db: AsyncSession, 
        experience_id: str,
        update_data: WorkExperienceUpdate
    ) -> WorkExperience:
        """
        Update employee work experience with business logic validation.
        
        Args:
            db: Database session
            experience_id: Unique identifier for work experience
            update_data: Data to update
            
        Returns:
            WorkExperience: Updated work experience object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_work_experience_data_update(update_data)
        
        # Update work experience
        updated_experience = await self.repository.update_employee_work_experience(
            db, experience_id, update_data
        )
        
        if not updated_experience:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Work experience not found with ID: {experience_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_experience
    
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
            bool: True if deletion successful
            
        Raises:
            AppException: If work experience not found
        """
        deleted = await self.repository.delete_employee_work_experience(
            db, experience_id
        )
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Work experience not found with ID: {experience_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
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
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[WorkExperience]: List of matching work experiences
            
        Raises:
            AppException: If validation fails
        """
        # Validate search parameters
        if not search_term or len(search_term.strip()) < 2:
            raise AppException(
                message_key=response_message.INVALID_REQUEST,
                details="Search term must be at least 2 characters long",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.search_work_experiences(
            db, search_term.strip(), skip, limit
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
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[WorkExperience]: List of current work experiences
            
        Raises:
            AppException: If validation fails
        """
        # Validate pagination parameters
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.get_current_work_experiences(db, skip, limit)
    
    async def get_work_experience_count(self, db: AsyncSession) -> int:
        """
        Get total count of work experience records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_work_experience_count(db)
    
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
        """
        return await self.repository.get_work_experience_count_by_employee(db, employee_id)
    
    # Private validation methods
    def _validate_work_experience_data_create(self, work_experience_data: WorkExperienceCreate) -> None:
        """
        Validate work experience creation data.
        
        Args:
            work_experience_data: Work experience data to validate
            
        Raises:
            AppException: If validation fails
        """
        if not work_experience_data.employee_id or not work_experience_data.employee_id.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Employee ID is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not work_experience_data.company_name or not work_experience_data.company_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Company name is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not work_experience_data.job_title or not work_experience_data.job_title.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Job title is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not work_experience_data.start_date:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Start date is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate date logic
        self._validate_date_logic(work_experience_data.start_date, work_experience_data.end_date)
        
        # Validate contact information if provided
        if work_experience_data.reference_contact:
            self._validate_phone_format(work_experience_data.reference_contact)
    
    def _validate_work_experience_data_update(self, update_data: WorkExperienceUpdate) -> None:
        """
        Validate work experience update data.
        
        Args:
            update_data: Work experience update data to validate
            
        Raises:
            AppException: If validation fails
        """
        # Validate company name if provided
        if update_data.company_name is not None and not update_data.company_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Company name cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate job title if provided
        if update_data.job_title is not None and not update_data.job_title.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Job title cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate date logic if both dates are provided
        if update_data.start_date and update_data.end_date:
            self._validate_date_logic(update_data.start_date, update_data.end_date)
        
        # Validate contact information if provided
        if update_data.reference_contact:
            self._validate_phone_format(update_data.reference_contact)
    
    def _validate_date_logic(self, start_date: date, end_date: Optional[date]) -> None:
        """
        Validate date logic for work experience.
        
        Args:
            start_date: Employment start date
            end_date: Employment end date (can be None for current job)
            
        Raises:
            AppException: If date validation fails
        """
        if end_date and start_date >= end_date:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="End date must be after start date",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if start date is not too far in the future
        from datetime import date as today_date
        if start_date > today_date.today():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Start date cannot be in the future",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if end date is not in the future (unless it's current job)
        if end_date and end_date > today_date.today():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="End date cannot be in the future",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def _validate_phone_format(self, phone: str) -> None:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            
        Raises:
            AppException: If phone format is invalid
        """
        # Basic phone validation - adjust pattern as needed
        phone_pattern = r'^\+?[\d\s\-\(\)]{7,25}$'
        
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        if not re.match(phone_pattern, clean_phone):
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Invalid phone number format",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def _validate_pagination_params(self, skip: int, limit: int) -> None:
        """
        Validate pagination parameters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Raises:
            AppException: If pagination parameters are invalid
        """
        if skip < 0:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Skip parameter must be non-negative",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if limit <= 0 or limit > 1000:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Limit parameter must be between 1 and 1000",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    async def _validate_employee_exists(self, db: AsyncSession, employee_id: str) -> None:
        """
        Validate that employee exists (placeholder - implement based on your employee model).
        
        Args:
            db: Database session
            employee_id: Employee ID to validate
            
        Raises:
            AppException: If employee doesn't exist
        """
        # TODO: Implement employee existence check
        # This would typically query your employee table
        # For now, we'll skip this validation
        pass