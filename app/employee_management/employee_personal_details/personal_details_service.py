from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_data.employee_personal_details_model import PersonalDetails
from app.employee_management.employee_personal_details.personal_details_schema import (
    PersonalDetailsCreate, 
    PersonalDetailsUpdate,
    PersonalDetailsResponse
)
from app.employee_management.employee_personal_details.personal_details_repository import (
    EmployeePersonalDetailsRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status

# Initialize response messages
response_message = ResponseMessage()


class EmployeePersonalDetailsService:
    """
    Service layer for employee personal details operations.
    Handles business logic, validation, and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmployeePersonalDetailsRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmployeePersonalDetailsRepository()
    
    async def create_employee_personal_details(
        self, 
        db: AsyncSession, 
        personal_data: PersonalDetailsCreate
    ) -> PersonalDetails:
        """
        Create new employee personal details with business logic validation.
        
        Args:
            db: Database session
            personal_data: Personal details data to create
            
        Returns:
            PersonalDetails: Created personal details object
            
        Raises:
            AppException: If validation fails or creation fails
        """
        # Validate required fields
        self._validate_personal_data_create(personal_data)
        
        # Validate business rules
        await self._validate_employee_exists(db, personal_data.employee_id)
        
        # Create personal details
        created_details = await self.repository.create_employee_personal_details(
            db, personal_data
        )
        
        return created_details
    
    async def get_employee_personal_details_by_id(
        self, 
        db: AsyncSession, 
        personal_details_id: str
    ) -> PersonalDetails:
        """
        Retrieve employee personal details by ID.
        
        Args:
            db: Database session
            personal_details_id: Unique identifier for personal details
            
        Returns:
            PersonalDetails: Personal details object
            
        Raises:
            AppException: If personal details not found
        """
        personal_details = await self.repository.get_employee_personal_details_by_id(
            db, personal_details_id
        )
        
        if not personal_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Personal details not found with ID: {personal_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return personal_details
    
    async def check_for_new_employee(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> PersonalDetails:
        """
        Retrieve employee personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            PersonalDetails: Personal details object
            
        Raises:
            AppException: If personal details not found
        """
        personal_details = await self.repository.get_employee_personal_details_by_employee_id(
            db, employee_id
        )
        
        if not personal_details:
            return False
        
        return True

    async def get_employee_personal_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> PersonalDetails:
        """
        Retrieve employee personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            PersonalDetails: Personal details object
            
        Raises:
            AppException: If personal details not found
        """
        print("----------------==========##########-->", employee_id)
        personal_details = await self.repository.get_employee_personal_details_by_employee_id(
            db, employee_id
        )
        
        if not personal_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Personal details not found for employee ID: {employee_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return personal_details
    
    async def get_all_employee_personal_details(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[PersonalDetails]:
        """
        Retrieve all employee personal details with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[PersonalDetails]: List of personal details objects
            
        Raises:
            AppException: If validation fails
        """
        # Validate pagination parameters
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.get_all_employee_personal_details(db, skip, limit)
    
    async def update_employee_personal_details(
        self, 
        db: AsyncSession, 
        personal_details_id: str,
        update_data: PersonalDetailsUpdate
    ) -> PersonalDetails:
        """
        Update employee personal details with business logic validation.
        
        Args:
            db: Database session
            personal_details_id: Unique identifier for personal details
            update_data: Data to update
            
        Returns:
            PersonalDetails: Updated personal details object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_personal_data_update(update_data)
        
        # Update personal details
        updated_details = await self.repository.update_employee_personal_details(
            db, personal_details_id, update_data
        )
        
        if not updated_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Personal details not found with ID: {personal_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_details
    
    async def update_employee_personal_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        update_data: PersonalDetailsUpdate
    ) -> PersonalDetails:
        """
        Update employee personal details by employee ID with business logic validation.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            update_data: Data to update
            
        Returns:
            PersonalDetails: Updated personal details object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_personal_data_update(update_data)
        
        # Update personal details by employee ID
        updated_details = await self.repository.update_employee_personal_details_by_employee_id(
            db, employee_id, update_data
        )
        
        if not updated_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Personal details not found for employee ID: {employee_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_details
    
    async def delete_employee_personal_details(
        self, 
        db: AsyncSession, 
        personal_details_id: str
    ) -> bool:
        """
        Delete employee personal details.
        
        Args:
            db: Database session
            personal_details_id: Unique identifier for personal details
            
        Returns:
            bool: True if deletion successful
            
        Raises:
            AppException: If personal details not found
        """
        deleted = await self.repository.delete_employee_personal_details(
            db, personal_details_id
        )
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Personal details not found with ID: {personal_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
    async def search_personal_details(
        self, 
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PersonalDetails]:
        """
        Search employee personal details by name or email.
        
        Args:
            db: Database session
            search_term: Term to search for
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[PersonalDetails]: List of matching personal details
            
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
        
        return await self.repository.search_personal_details(
            db, search_term.strip(), skip, limit
        )
    
    async def get_personal_details_count(self, db: AsyncSession) -> int:
        """
        Get total count of personal details records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_personal_details_count(db)
    
    # Private validation methods
    def _validate_personal_data_create(self, personal_data: PersonalDetailsCreate) -> None:
        """
        Validate personal details creation data.
        
        Args:
            personal_data: Personal details data to validate
            
        Raises:
            AppException: If validation fails
        """
        if not personal_data.employee_id or not personal_data.employee_id.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Employee ID is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not personal_data.first_name or not personal_data.first_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="First name is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not personal_data.last_name or not personal_data.last_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Last name is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate email format if provided
        if personal_data.personal_email:
            self._validate_email_format(personal_data.personal_email)
        
        # Validate phone numbers if provided
        if personal_data.personal_contact_number:
            self._validate_phone_format(personal_data.personal_contact_number)
        
        if personal_data.emergency_contact_number:
            self._validate_phone_format(personal_data.emergency_contact_number)
    
    def _validate_personal_data_update(self, update_data: PersonalDetailsUpdate) -> None:
        """
        Validate personal details update data.
        
        Args:
            update_data: Personal details update data to validate
            
        Raises:
            AppException: If validation fails
        """
        # Validate email format if provided
        if update_data.personal_email:
            self._validate_email_format(update_data.personal_email)
        
        # Validate phone numbers if provided
        if update_data.personal_contact_number:
            self._validate_phone_format(update_data.personal_contact_number)
        
        if update_data.emergency_contact_number:
            self._validate_phone_format(update_data.emergency_contact_number)
        
        # Validate names if provided
        if update_data.first_name is not None and not update_data.first_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="First name cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if update_data.last_name is not None and not update_data.last_name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Last name cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def _validate_email_format(self, email: str) -> None:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Raises:
            AppException: If email format is invalid
        """
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Invalid email format",
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
        import re
        # Basic phone validation - adjust pattern as needed
        phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
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