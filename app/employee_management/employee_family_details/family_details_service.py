from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_data.employee_family_details_model import FamilyDetails
from app.employee_management.employee_family_details.family_details_schema import (
    FamilyDetailsCreate, 
    FamilyDetailsUpdate,
    FamilyDetailsResponse
)
from app.employee_management.employee_family_details.family_details_repository import (
    EmployeeFamilyDetailsRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status

# Initialize response messages
response_message = ResponseMessage()


class EmployeeFamilyDetailsService:
    """
    Service layer for employee family details operations.
    Handles business logic, validation, and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmployeeFamilyDetailsRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmployeeFamilyDetailsRepository()
    
    async def create_employee_family_details(
        self, 
        db: AsyncSession, 
        family_data: FamilyDetailsCreate
    ) -> FamilyDetails:
        """
        Create new employee family details with business logic validation.
        
        Args:
            db: Database session
            family_data: Family details data to create
            
        Returns:
            FamilyDetails: Created family details object
            
        Raises:
            AppException: If validation fails or creation fails
        """
        # Validate required fields
        self._validate_family_data_create(family_data)
        
        # Validate business rules
        await self._validate_employee_exists(db, family_data.employee_id)
        
        # Create family details
        created_details = await self.repository.create_employee_family_details(
            db, family_data
        )
        
        return created_details
    
    async def get_employee_family_details_by_id(
        self, 
        db: AsyncSession, 
        family_details_id: str
    ) -> FamilyDetails:
        """
        Retrieve employee family details by ID.
        
        Args:
            db: Database session
            family_details_id: Unique identifier for family details
            
        Returns:
            FamilyDetails: Family details object
            
        Raises:
            AppException: If family details not found
        """
        family_details = await self.repository.get_employee_family_details_by_id(
            db, family_details_id
        )
        
        if not family_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Family details not found with ID: {family_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return family_details
    
    async def check_for_new_employee(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> bool:
        """
        Check if employee has family details.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            bool: True if family details exist, False otherwise
        """
        family_details = await self.repository.check_for_new_employee(
            db, employee_id
        )
        
        return family_details is not None

    async def get_employee_family_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> FamilyDetails:
        """
        Retrieve employee family details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            FamilyDetails: Family details object
            
        Raises:
            AppException: If family details not found
        """
        family_details = await self.repository.get_employee_family_details_by_employee_id(
            db, employee_id
        )
        
        if not family_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Family details not found for employee ID: {employee_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return family_details
    
    async def get_all_employee_family_details(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[FamilyDetails]:
        """
        Retrieve all employee family details with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[FamilyDetails]: List of family details objects
            
        Raises:
            AppException: If validation fails
        """
        # Validate pagination parameters
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.get_all_employee_family_details(db, skip, limit)
    
    async def update_employee_family_details(
        self, 
        db: AsyncSession, 
        family_details_id: str,
        update_data: FamilyDetailsUpdate
    ) -> FamilyDetails:
        """
        Update employee family details with business logic validation.
        
        Args:
            db: Database session
            family_details_id: Unique identifier for family details
            update_data: Data to update
            
        Returns:
            FamilyDetails: Updated family details object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_family_data_update(update_data)
        
        # Update family details
        updated_details = await self.repository.update_employee_family_details(
            db, family_details_id, update_data
        )
        
        if not updated_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Family details not found with ID: {family_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_details
    
    async def update_employee_family_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        update_data: FamilyDetailsUpdate
    ) -> FamilyDetails:
        """
        Update employee family details by employee ID with business logic validation.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            update_data: Data to update
            
        Returns:
            FamilyDetails: Updated family details object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_family_data_update(update_data)
        
        # Update family details by employee ID
        updated_details = await self.repository.update_employee_family_details_by_employee_id(
            db, employee_id, update_data
        )
        
        if not updated_details:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Family details not found for employee ID: {employee_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_details
    
    async def delete_employee_family_details(
        self, 
        db: AsyncSession, 
        family_details_id: str
    ) -> bool:
        """
        Delete employee family details.
        
        Args:
            db: Database session
            family_details_id: Unique identifier for family details
            
        Returns:
            bool: True if deletion successful
            
        Raises:
            AppException: If family details not found
        """
        deleted = await self.repository.delete_employee_family_details(
            db, family_details_id
        )
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Family details not found with ID: {family_details_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
    async def search_family_details(
        self, 
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FamilyDetails]:
        """
        Search employee family details by family member names.
        
        Args:
            db: Database session
            search_term: Term to search for
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[FamilyDetails]: List of matching family details
            
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
        
        return await self.repository.search_family_details(
            db, search_term.strip(), skip, limit
        )
    
    async def get_family_details_count(self, db: AsyncSession) -> int:
        """
        Get total count of family details records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_family_details_count(db)
    
    # Private validation methods
    def _validate_family_data_create(self, family_data: FamilyDetailsCreate) -> None:
        """
        Validate family details creation data.
        
        Args:
            family_data: Family details data to validate
            
        Raises:
            AppException: If validation fails
        """
        if not family_data.employee_id or not family_data.employee_id.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Employee ID is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate father details if provided
        if family_data.is_father:
            if not family_data.father_name or not family_data.father_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Father name is required when father details are provided",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            if family_data.father_date_of_birth:
                self._validate_birth_date(family_data.father_date_of_birth, "Father")
            
            if family_data.father_contact_number:
                self._validate_phone_format(family_data.father_contact_number, "Father")
        
        # Validate mother details if provided
        if family_data.is_mother:
            if not family_data.mother_name or not family_data.mother_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Mother name is required when mother details are provided",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            if family_data.mother_date_of_birth:
                self._validate_birth_date(family_data.mother_date_of_birth, "Mother")
            
            if family_data.mother_contact_number:
                self._validate_phone_format(family_data.mother_contact_number, "Mother")
        
        # Validate spouse details if provided
        if family_data.is_spouse:
            if not family_data.spouse_name or not family_data.spouse_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Spouse name is required when spouse details are provided",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            if family_data.spouse_date_of_birth:
                self._validate_birth_date(family_data.spouse_date_of_birth, "Spouse")
            
            if family_data.spouse_contact_number:
                self._validate_phone_format(family_data.spouse_contact_number, "Spouse")
        
        # Validate children details if provided
        if family_data.is_children:
            if not family_data.children_name or not family_data.children_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Children name is required when children details are provided",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate siblings details if provided
        if family_data.is_siblings:
            if not family_data.sibling_names or not family_data.sibling_names.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Sibling names are required when sibling details are provided",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
    
    def _validate_family_data_update(self, update_data: FamilyDetailsUpdate) -> None:
        """
        Validate family details update data.
        
        Args:
            update_data: Family details update data to validate
            
        Raises:
            AppException: If validation fails
        """
        # Validate father details if being updated
        if update_data.is_father and update_data.father_name is not None:
            if not update_data.father_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Father name cannot be empty when father details are enabled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        if update_data.father_date_of_birth:
            self._validate_birth_date(update_data.father_date_of_birth, "Father")
        
        if update_data.father_contact_number:
            self._validate_phone_format(update_data.father_contact_number, "Father")
        
        # Validate mother details if being updated
        if update_data.is_mother and update_data.mother_name is not None:
            if not update_data.mother_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Mother name cannot be empty when mother details are enabled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        if update_data.mother_date_of_birth:
            self._validate_birth_date(update_data.mother_date_of_birth, "Mother")
        
        if update_data.mother_contact_number:
            self._validate_phone_format(update_data.mother_contact_number, "Mother")
        
        # Validate spouse details if being updated
        if update_data.is_spouse and update_data.spouse_name is not None:
            if not update_data.spouse_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Spouse name cannot be empty when spouse details are enabled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        if update_data.spouse_date_of_birth:
            self._validate_birth_date(update_data.spouse_date_of_birth, "Spouse")
        
        if update_data.spouse_contact_number:
            self._validate_phone_format(update_data.spouse_contact_number, "Spouse")
        
        # Validate children details if being updated
        if update_data.is_children and update_data.children_name is not None:
            if not update_data.children_name.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Children name cannot be empty when children details are enabled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate siblings details if being updated
        if update_data.is_siblings and update_data.sibling_names is not None:
            if not update_data.sibling_names.strip():
                raise AppException(
                    message_key=response_message.VALIDATION_ERROR,
                    details="Sibling names cannot be empty when sibling details are enabled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
    
    def _validate_birth_date(self, birth_date: date, person_type: str) -> None:
        """
        Validate birth date.
        
        Args:
            birth_date: Birth date to validate
            person_type: Type of person (Father, Mother, Spouse, etc.)
            
        Raises:
            AppException: If birth date is invalid
        """
        from datetime import date as date_today
        
        if birth_date > date_today.today():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details=f"{person_type} birth date cannot be in the future",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for reasonable age limits (e.g., not older than 150 years)
        from datetime import timedelta
        max_age_date = date_today.today() - timedelta(days=150*365)
        if birth_date < max_age_date:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details=f"{person_type} birth date seems too old",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def _validate_phone_format(self, phone: str, person_type: str) -> None:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            person_type: Type of person (Father, Mother, Spouse, etc.)
            
        Raises:
            AppException: If phone format is invalid
        """
        import re
        # Basic phone validation - adjust pattern as needed
        phone_pattern = r'^\+?[\d\s\-\(\)]{10,20}$'
        if not re.match(phone_pattern, phone):
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details=f"Invalid {person_type.lower()} phone number format",
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