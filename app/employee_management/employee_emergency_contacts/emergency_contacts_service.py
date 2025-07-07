from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_data.employee_emergency_contacts_model import EmergencyContact
from app.employee_management.employee_emergency_contacts.emergency_contacts_schema import (
    EmergencyContactCreate, 
    EmergencyContactUpdate,
    EmergencyContactResponse
)
from app.employee_management.employee_emergency_contacts.emergency_contacts_repository import (
    EmergencyContactRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status

# Initialize response messages
response_message = ResponseMessage()


class EmergencyContactService:
    """
    Service layer for emergency contact operations.
    Handles business logic, validation, and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmergencyContactRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmergencyContactRepository()
    
    async def create_emergency_contact(
        self, 
        db: AsyncSession, 
        contact_data: EmergencyContactCreate
    ) -> EmergencyContact:
        """
        Create new emergency contact with business logic validation.
        
        Args:
            db: Database session
            contact_data: Emergency contact data to create
            
        Returns:
            EmergencyContact: Created emergency contact object
            
        Raises:
            AppException: If validation fails or creation fails
        """
        # Validate required fields
        self._validate_contact_data_create(contact_data)
        
        # Validate business rules
        await self._validate_employee_exists(db, contact_data.employee_id)
        await self._validate_contact_limits(db, contact_data.employee_id)
        
        # Create emergency contact
        created_contact = await self.repository.create_emergency_contact(db, contact_data)
        
        return created_contact
    
    async def get_emergency_contact_by_id(
        self, 
        db: AsyncSession, 
        contact_id: str
    ) -> EmergencyContact:
        """
        Retrieve emergency contact by ID.
        
        Args:
            db: Database session
            contact_id: Unique identifier for emergency contact
            
        Returns:
            EmergencyContact: Emergency contact object
            
        Raises:
            AppException: If emergency contact not found
        """
        contact = await self.repository.get_emergency_contact_by_id(db, contact_id)
        
        if not contact:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Emergency contact not found with ID: {contact_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return contact
    
    async def get_emergency_contacts_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[EmergencyContact]:
        """
        Retrieve all emergency contacts for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            List[EmergencyContact]: List of emergency contacts
        """
        print("----------------==========##########-->", employee_id)
        emergency_contacts = await self.repository.get_emergency_contacts_by_employee_id(db, employee_id)
        return emergency_contacts
    
    async def get_all_emergency_contacts(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmergencyContact]:
        """
        Retrieve all emergency contacts with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[EmergencyContact]: List of emergency contacts
            
        Raises:
            AppException: If validation fails
        """
        # Validate pagination parameters
        self._validate_pagination_params(skip, limit)
        
        return await self.repository.get_all_emergency_contacts(db, skip, limit)
    
    async def update_emergency_contact(
        self, 
        db: AsyncSession, 
        contact_id: str,
        update_data: EmergencyContactUpdate
    ) -> EmergencyContact:
        """
        Update emergency contact with business logic validation.
        
        Args:
            db: Database session
            contact_id: Unique identifier for emergency contact
            update_data: Data to update
            
        Returns:
            EmergencyContact: Updated emergency contact object
            
        Raises:
            AppException: If validation fails or update fails
        """
        # Validate update data
        self._validate_contact_data_update(update_data)
        
        # Update emergency contact
        updated_contact = await self.repository.update_emergency_contact(
            db, contact_id, update_data
        )
        
        if not updated_contact:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Emergency contact not found with ID: {contact_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_contact
    
    async def delete_emergency_contact(
        self, 
        db: AsyncSession, 
        contact_id: str
    ) -> bool:
        """
        Delete emergency contact.
        
        Args:
            db: Database session
            contact_id: Unique identifier for emergency contact
            
        Returns:
            bool: True if deletion successful
            
        Raises:
            AppException: If emergency contact not found
        """
        deleted = await self.repository.delete_emergency_contact(db, contact_id)
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Emergency contact not found with ID: {contact_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
    async def delete_all_emergency_contacts_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> int:
        """
        Delete all emergency contacts for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            int: Number of deleted records
        """
        return await self.repository.delete_all_emergency_contacts_by_employee_id(db, employee_id)
    
    async def search_emergency_contacts(
        self, 
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmergencyContact]:
        """
        Search emergency contacts by name or phone number.
        
        Args:
            db: Database session
            search_term: Term to search for
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[EmergencyContact]: List of matching emergency contacts
            
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
        
        return await self.repository.search_emergency_contacts(
            db, search_term.strip(), skip, limit
        )
    
    async def get_emergency_contacts_count(self, db: AsyncSession) -> int:
        """
        Get total count of emergency contacts records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_emergency_contacts_count(db)
    
    async def get_emergency_contacts_count_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> int:
        """
        Get count of emergency contacts for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            int: Count of emergency contacts for the employee
        """
        return await self.repository.get_emergency_contacts_count_by_employee_id(db, employee_id)
    
    # Private validation methods
    def _validate_contact_data_create(self, contact_data: EmergencyContactCreate) -> None:
        """
        Validate emergency contact creation data.
        
        Args:
            contact_data: Emergency contact data to validate
            
        Raises:
            AppException: If validation fails
        """
        if not contact_data.employee_id or not contact_data.employee_id.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Employee ID is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not contact_data.name or not contact_data.name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Contact name is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not contact_data.relationship or not contact_data.relationship.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Relationship is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if not contact_data.primary_phone or not contact_data.primary_phone.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Primary phone number is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate phone numbers
        self._validate_phone_format(contact_data.primary_phone)
        if contact_data.secondary_phone:
            self._validate_phone_format(contact_data.secondary_phone)
        
        # Validate email if provided
        if contact_data.email:
            self._validate_email_format(contact_data.email)
    
    def _validate_contact_data_update(self, update_data: EmergencyContactUpdate) -> None:
        """
        Validate emergency contact update data.
        
        Args:
            update_data: Emergency contact update data to validate
            
        Raises:
            AppException: If validation fails
        """
        # Validate names if provided
        if update_data.name is not None and not update_data.name.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Contact name cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if update_data.relationship is not None and not update_data.relationship.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Relationship cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if update_data.primary_phone is not None and not update_data.primary_phone.strip():
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details="Primary phone number cannot be empty",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate phone numbers if provided
        if update_data.primary_phone:
            self._validate_phone_format(update_data.primary_phone)
        
        if update_data.secondary_phone:
            self._validate_phone_format(update_data.secondary_phone)
        
        # Validate email if provided
        if update_data.email:
            self._validate_email_format(update_data.email)
    
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
    
    async def _validate_contact_limits(self, db: AsyncSession, employee_id: str) -> None:
        """
        Validate contact limits for an employee (e.g., maximum 5 contacts).
        
        Args:
            db: Database session
            employee_id: Employee ID to validate
            
        Raises:
            AppException: If contact limit exceeded
        """
        # Check current contact count
        current_count = await self.repository.get_emergency_contacts_count_by_employee_id(db, employee_id)
        
        # Set maximum contacts limit (adjust as needed)
        max_contacts = 5
        
        if current_count >= max_contacts:
            raise AppException(
                message_key=response_message.VALIDATION_ERROR,
                details=f"Maximum {max_contacts} emergency contacts allowed per employee",
                status_code=status.HTTP_400_BAD_REQUEST
            )