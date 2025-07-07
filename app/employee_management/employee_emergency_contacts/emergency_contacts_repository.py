from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_emergency_contacts_model import EmergencyContact
from app.employee_management.employee_emergency_contacts.emergency_contacts_schema import (
    EmergencyContactCreate, 
    EmergencyContactUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmergencyContactRepository:
    """
    Repository class for handling all database operations related to emergency contacts.
    Implements full CRUD operations with proper error handling and validation.
    """

    async def create_emergency_contact(
        self, 
        db: AsyncSession, 
        contact_data: EmergencyContactCreate
    ) -> EmergencyContact:
        """
        Create new emergency contact.
        
        Args:
            db: Database session
            contact_data: Emergency contact data to create
            
        Returns:
            EmergencyContact: Created emergency contact object
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Create new emergency contact
            new_contact = EmergencyContact(**contact_data.model_dump())
            db.add(new_contact)
            await db.commit()
            await db.refresh(new_contact)
            
            return new_contact
            
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

    async def get_emergency_contact_by_id(
        self, 
        db: AsyncSession, 
        contact_id: str
    ) -> Optional[EmergencyContact]:
        """
        Retrieve emergency contact by contact ID.
        
        Args:
            db: Database session
            contact_id: Unique identifier for emergency contact
            
        Returns:
            EmergencyContact or None: Emergency contact object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(EmergencyContact).where(EmergencyContact.contact_id == contact_id)
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve emergency contact: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(EmergencyContact).where(
                EmergencyContact.employee_id == employee_id
            ).order_by(EmergencyContact.priority_order)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve emergency contacts for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[EmergencyContact]: List of emergency contacts
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(EmergencyContact).offset(skip).limit(limit).order_by(
                EmergencyContact.employee_id, EmergencyContact.priority_order
            )
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve emergency contacts list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_emergency_contact(
        self, 
        db: AsyncSession, 
        contact_id: str,
        update_data: EmergencyContactUpdate
    ) -> Optional[EmergencyContact]:
        """
        Update emergency contact.
        
        Args:
            db: Database session
            contact_id: Unique identifier for emergency contact
            update_data: Data to update
            
        Returns:
            EmergencyContact or None: Updated emergency contact object
            
        Raises:
            AppException: If emergency contact not found or database error occurs
        """
        try:
            # Check if emergency contact exists
            existing_contact = await self.get_emergency_contact_by_id(db, contact_id)
            
            if not existing_contact:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Emergency contact not found with ID: {contact_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_contact
            
            # Perform update
            query = (
                update(EmergencyContact)
                .where(EmergencyContact.contact_id == contact_id)
                .values(**update_dict)
                .returning(EmergencyContact)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_contact = result.scalar_one_or_none()
            if updated_contact:
                await db.refresh(updated_contact)
            
            return updated_contact
            
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
                details=f"Failed to update emergency contact: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if emergency contact exists
            existing_contact = await self.get_emergency_contact_by_id(db, contact_id)
            
            if not existing_contact:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Emergency contact not found with ID: {contact_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete emergency contact
            query = delete(EmergencyContact).where(EmergencyContact.contact_id == contact_id)
            
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete emergency contact: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = delete(EmergencyContact).where(EmergencyContact.employee_id == employee_id)
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete emergency contacts for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[EmergencyContact]: List of matching emergency contacts
            
        Raises:
            AppException: If database error occurs
        """
        try:
            search_pattern = f"%{search_term.lower()}%"
            
            query = select(EmergencyContact).where(
                (EmergencyContact.name.ilike(search_pattern)) |
                (EmergencyContact.primary_phone.ilike(search_pattern)) |
                (EmergencyContact.secondary_phone.ilike(search_pattern)) |
                (EmergencyContact.email.ilike(search_pattern))
            ).offset(skip).limit(limit).order_by(
                EmergencyContact.employee_id, EmergencyContact.priority_order
            )
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Search operation failed: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_emergency_contacts_count(self, db: AsyncSession) -> int:
        """
        Get total count of emergency contacts records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(EmergencyContact.contact_id))
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(EmergencyContact.contact_id)).where(
                EmergencyContact.employee_id == employee_id
            )
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )