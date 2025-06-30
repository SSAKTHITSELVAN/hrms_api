from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_address_model import Address
from app.employee_management.employee_address.address_schema import (
    AddressCreate, 
    AddressUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmployeeAddressRepository:
    """
    Repository class for handling all database operations related to employee addresses.
    Implements full CRUD operations with proper error handling.
    """

    async def create_employee_address(
        self, 
        db: AsyncSession, 
        address_data: AddressCreate
    ) -> Address:
        """
        Create new employee address.
        
        Args:
            db: Database session
            address_data: Address data to create
            
        Returns:
            Address: Created address object
            
        Raises:
            AppException: If database error occurs or address type already exists for employee
        """
        try:
            # Check if employee already has an address of this type
            existing_address = await self.get_address_by_employee_and_type(
                db, address_data.employee_id, address_data.address_type
            )
            
            if existing_address:
                raise AppException(
                    message_key="ADDRESS_TYPE_EXISTS",
                    details=f"Employee already has a {address_data.address_type} address. Only one address per type is allowed.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            new_address = Address(**address_data.model_dump())
            db.add(new_address)
            await db.commit()
            await db.refresh(new_address)
            
            return new_address
            
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

    async def get_employee_address_by_id(
        self, 
        db: AsyncSession, 
        address_id: str
    ) -> Optional[Address]:
        """
        Retrieve employee address by address ID.
        
        Args:
            db: Database session
            address_id: Unique identifier for address
            
        Returns:
            Address or None: Address object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Address).where(Address.address_id == address_id)
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve address: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Address).where(Address.employee_id == employee_id)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve addresses for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Address]: List of address objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Address).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve addresses list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_address(
        self, 
        db: AsyncSession, 
        address_id: str,
        update_data: AddressUpdate
    ) -> Optional[Address]:
        """
        Update employee address.
        
        Args:
            db: Database session
            address_id: Unique identifier for address
            update_data: Data to update
            
        Returns:
            Address or None: Updated address object
            
        Raises:
            AppException: If address not found or database error occurs
        """
        try:
            # Check if address exists
            existing_address = await self.get_employee_address_by_id(db, address_id)
            
            if not existing_address:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Address not found with ID: {address_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_address
            
            # If address_type is being updated, check for duplicates
            if 'address_type' in update_dict:
                existing_type_address = await self.get_address_by_employee_and_type(
                    db, existing_address.employee_id, update_dict['address_type']
                )
                
                if existing_type_address and existing_type_address.address_id != address_id:
                    raise AppException(
                        message_key="ADDRESS_TYPE_EXISTS",
                        details=f"Employee already has a {update_dict['address_type']} address. Only one address per type is allowed.",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            
            # Perform update
            query = (
                update(Address)
                .where(Address.address_id == address_id)
                .values(**update_dict)
                .returning(Address)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_address = result.scalar_one_or_none()
            if updated_address:
                await db.refresh(updated_address)
            
            return updated_address
            
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
                details=f"Failed to update address: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_address_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: str,
        update_data: AddressUpdate
    ) -> Optional[Address]:
        """
        Update employee address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address to update
            update_data: Data to update
            
        Returns:
            Address or None: Updated address object
            
        Raises:
            AppException: If address not found or database error occurs
        """
        try:
            # Find the address by employee_id and address_type
            existing_address = await self.get_address_by_employee_and_type(
                db, employee_id, address_type
            )
            
            if not existing_address:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"No {address_type} address found for employee: {employee_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                raise AppException(
                    message_key=response_message.BAD_REQUEST,
                    details="No data provided for update.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Apply updates
            for key, value in update_dict.items():
                setattr(existing_address, key, value)

            await db.commit()
            await db.refresh(existing_address)

            return existing_address
            
    
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
                details=f"Failed to update address: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    async def check_employee_address_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: str
    ) -> Optional[Address]:
        """
        Update employee address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address to update
            update_data: Data to update
            
        Returns:
            Address or None: Updated address object
            
        Raises:
            AppException: If address not found or database error occurs
        """
        try:
            # Find the address by employee_id and address_type
            existing_address = await self.get_address_by_employee_and_type(
                db, employee_id, address_type
            )
            
            if existing_address:
                return True
            
            return False
            
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
                details=f"Failed to update address: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if address exists
            existing_address = await self.get_employee_address_by_id(db, address_id)
            
            if not existing_address:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Address not found with ID: {address_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete address
            query = delete(Address).where(Address.address_id == address_id)
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete address: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_addresses_count(self, db: AsyncSession) -> int:
        """
        Get total count of address records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(Address.address_id))
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_addresses_by_type(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: str
    ) -> List[Address]:
        """
        Get addresses by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address
            
        Returns:
            List[Address]: List of matching addresses
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(Address).where(
                and_(
                    Address.employee_id == employee_id,
                    Address.address_type == address_type
                )
            )
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve addresses by type: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_address_by_employee_and_type(
        self, 
        db: AsyncSession, 
        employee_id: str,
        address_type: str
    ) -> Optional[Address]:
        """
        Get single address by employee ID and address type.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            address_type: Type of address
            
        Returns:
            Address or None: Address object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            print("-------------wo---------------------=========]]]]]]]]]")
            query = select(Address).where(
                and_(
                    Address.employee_id == employee_id,
                    Address.address_type == address_type
                )
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve address by employee and type: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )