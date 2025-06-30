from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_data.employee_address_model import Address
from app.employee_management.employee_address.address_schema import (
    AddressCreate, 
    AddressUpdate,
    AddressResponse,
    AddressType
)
from app.employee_management.employee_address.address_repository import (
    EmployeeAddressRepository
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage
from fastapi import status

# Initialize response messages
response_message = ResponseMessage()


class EmployeeAddressService:
    """
    Service layer for employee address operations.
    Handles business logic and orchestrates repository operations.
    """
    
    def __init__(self, repository: EmployeeAddressRepository = None) -> None:
        """
        Initialize the service with optional repository dependency injection.
        
        Args:
            repository: Optional repository instance for testing purposes
        """
        self.repository = repository or EmployeeAddressRepository()
    
    async def create_employee_address(
        self, 
        db: AsyncSession, 
        address_data: AddressCreate
    ) -> Address:
        """
        Create new employee address with validation for unique address type per employee.
        
        Args:
            db: Database session
            address_data: Address data to create
            
        Returns:
            Address: Created address object
            
        Raises:
            AppException: If employee already has address of this type
        """
        return await self.repository.create_employee_address(db, address_data)
    
    async def get_employee_address_by_id(
        self, 
        db: AsyncSession, 
        address_id: str
    ) -> Address:
        """
        Retrieve employee address by ID.
        
        Args:
            db: Database session
            address_id: Unique identifier for address
            
        Returns:
            Address: Address object
            
        Raises:
            AppException: If address not found
        """
        address = await self.repository.get_employee_address_by_id(db, address_id)
        
        if not address:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Address not found with ID: {address_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return address
    
    async def get_employee_addresses_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[Address]:
        """
        Retrieve all employee addresses by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            List[Address]: List of address objects
        """
        return await self.repository.get_employee_addresses_by_employee_id(db, employee_id)
    
    async def get_all_employee_addresses(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Address]:
        """
        Retrieve all employee addresses with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[Address]: List of address objects
        """
        return await self.repository.get_all_employee_addresses(db, skip, limit)
    
    async def update_employee_address(
        self, 
        db: AsyncSession, 
        address_id: str,
        update_data: AddressUpdate
    ) -> Address:
        """
        Update employee address by address ID.
        
        Args:
            db: Database session
            address_id: Unique identifier for address
            update_data: Data to update
            
        Returns:
            Address: Updated address object
            
        Raises:
            AppException: If address not found or update fails
        """
        updated_address = await self.repository.update_employee_address(
            db, address_id, update_data
        )
        
        if not updated_address:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Address not found with ID: {address_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_address
    
    async def update_employee_address_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: AddressType,
        update_data: AddressUpdate
    ) -> Address:
        """
        Update employee address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address to update
            update_data: Data to update
            
        Returns:
            Address: Updated address object
            
        Raises:
            AppException: If address not found or update fails
        """
        print("-----ser---------=======>", update_data)
        updated_address = await self.repository.update_employee_address_by_employee_id(
            db, employee_id, address_type.value, update_data
        )
        
        if not updated_address:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"No {address_type.value} address found for employee: {employee_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return updated_address
    
    async def check_employee_address_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: AddressType,
    ) -> Address:
        """
        Update employee address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address to update
            
        Returns:
            Address: Updated address object
            
        Raises:
            AppException: If address not found or update fails
        """
        updated_address = await self.repository.check_employee_address_by_employee_id(
            db, employee_id, address_type.value
        )
        
        if not updated_address:
            return False
        
        return True
    
    async def delete_employee_address(
        self, 
        db: AsyncSession, 
        address_id: str
    ) -> bool:
        """
        Delete employee address.
        
        Args:
            db: Database session
            address_id: Unique identifier for address
            
        Returns:
            bool: True if deletion successful
            
        Raises:
            AppException: If address not found
        """
        deleted = await self.repository.delete_employee_address(db, address_id)
        
        if not deleted:
            raise AppException(
                message_key=response_message.RESOURCE_NOT_FOUND,
                details=f"Address not found with ID: {address_id}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return deleted
    
    async def get_addresses_count(self, db: AsyncSession) -> int:
        """
        Get total count of address records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
        """
        return await self.repository.get_addresses_count(db)
    
    async def get_addresses_by_type(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: AddressType
    ) -> List[Address]:
        """
        Get addresses by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address
            
        Returns:
            List[Address]: List of matching addresses
        """
        return await self.repository.get_addresses_by_type(db, employee_id, address_type.value)
    
    async def get_address_by_employee_and_type(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: AddressType
    ) -> Optional[Address]:
        """
        Get single address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address
            
        Returns:
            Address or None: Address object if found
        """
        return await self.repository.get_address_by_employee_and_type(
            db, employee_id, address_type.value
        )