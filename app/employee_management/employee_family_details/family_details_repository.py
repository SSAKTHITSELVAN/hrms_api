from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_family_details_model import FamilyDetails
from app.employee_management.employee_family_details.family_details_schema import (
    FamilyDetailsCreate, 
    FamilyDetailsUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmployeeFamilyDetailsRepository:
    """
    Repository class for handling all database operations related to employee family details.
    Implements full CRUD operations with proper error handling and validation.
    """

    async def create_employee_family_details(
        self, 
        db: AsyncSession, 
        family_data: FamilyDetailsCreate
    ) -> FamilyDetails:
        """
        Create new employee family details after checking for uniqueness.
        
        Args:
            db: Database session
            family_data: Family details data to create
            
        Returns:
            FamilyDetails: Created family details object
            
        Raises:
            AppException: If employee already has family details or database error occurs
        """
        try:
            # Check if family details already exist for this employee
            existing_details = await self._get_by_employee_id(db, family_data.employee_id)
            
            if existing_details:
                raise AppException(
                    message_key=response_message.FORBIDDEN_ACCESS,
                    details=f"Family details already exist for employee ID: {family_data.employee_id}",
                    status_code=status.HTTP_409_CONFLICT
                )
            
            # Create new family details
            new_family_details = FamilyDetails(**family_data.model_dump())
            db.add(new_family_details)
            await db.commit()
            await db.refresh(new_family_details)
            
            return new_family_details
            
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

    async def get_employee_family_details_by_id(
        self, 
        db: AsyncSession, 
        family_details_id: str
    ) -> Optional[FamilyDetails]:
        """
        Retrieve employee family details by family details ID.
        
        Args:
            db: Database session
            family_details_id: Unique identifier for family details
            
        Returns:
            FamilyDetails or None: Family details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(FamilyDetails).where(
                FamilyDetails.family_details_id == family_details_id
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve family details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def check_for_new_employee(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> Optional[FamilyDetails]:
        """
        Retrieve employee family details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            FamilyDetails or None: Family details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            return await self._get_by_employee_id(db, employee_id)
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve family details for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_employee_family_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> Optional[FamilyDetails]:
        """
        Retrieve employee family details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            FamilyDetails or None: Family details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            return await self._get_by_employee_id(db, employee_id)
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve family details for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[FamilyDetails]: List of family details objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(FamilyDetails).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve family details list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_family_details(
        self, 
        db: AsyncSession, 
        family_details_id: str,
        update_data: FamilyDetailsUpdate
    ) -> Optional[FamilyDetails]:
        """
        Update employee family details.
        
        Args:
            db: Database session
            family_details_id: Unique identifier for family details
            update_data: Data to update
            
        Returns:
            FamilyDetails or None: Updated family details object
            
        Raises:
            AppException: If family details not found or database error occurs
        """
        try:
            # Check if family details exist
            existing_details = await self.get_employee_family_details_by_id(
                db, family_details_id
            )
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Family details not found with ID: {family_details_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_details
            
            # Perform update
            query = (
                update(FamilyDetails)
                .where(FamilyDetails.family_details_id == family_details_id)
                .values(**update_dict)
                .returning(FamilyDetails)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_details = result.scalar_one_or_none()
            if updated_details:
                await db.refresh(updated_details)
            
            return updated_details
            
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
                details=f"Failed to update family details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_family_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        update_data: FamilyDetailsUpdate
    ) -> Optional[FamilyDetails]:
        """
        Update employee family details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            update_data: Data to update
            
        Returns:
            FamilyDetails or None: Updated family details object
            
        Raises:
            AppException: If family details not found or database error occurs
        """
        try:
            # Check if family details exist for this employee
            existing_details = await self._get_by_employee_id(db, employee_id)
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Family details not found for employee ID: {employee_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_details
            
            # Perform update
            query = (
                update(FamilyDetails)
                .where(FamilyDetails.employee_id == employee_id)
                .values(**update_dict)
                .returning(FamilyDetails)
            )
            
            result = await db.execute(query)
            await db.commit()
            
            updated_details = result.scalar_one_or_none()
            if updated_details:
                await db.refresh(updated_details)
            
            return updated_details
            
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
                details=f"Failed to update family details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if family details exist
            existing_details = await self.get_employee_family_details_by_id(
                db, family_details_id
            )
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Family details not found with ID: {family_details_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete family details
            query = delete(FamilyDetails).where(
                FamilyDetails.family_details_id == family_details_id
            )
            
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete family details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[FamilyDetails]: List of matching family details
            
        Raises:
            AppException: If database error occurs
        """
        try:
            search_pattern = f"%{search_term.lower()}%"
            
            query = select(FamilyDetails).where(
                (FamilyDetails.father_name.ilike(search_pattern)) |
                (FamilyDetails.mother_name.ilike(search_pattern)) |
                (FamilyDetails.spouse_name.ilike(search_pattern)) |
                (FamilyDetails.children_name.ilike(search_pattern)) |
                (FamilyDetails.sibling_names.ilike(search_pattern))
            ).offset(skip).limit(limit)
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Search operation failed: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_family_details_count(self, db: AsyncSession) -> int:
        """
        Get total count of family details records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(FamilyDetails.family_details_id))
            result = await db.execute(query)
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to get count: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Private helper methods
    async def _get_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> Optional[FamilyDetails]:
        """
        Private method to get family details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            FamilyDetails or None: Family details object if found
        """
        query = select(FamilyDetails).where(FamilyDetails.employee_id == employee_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()