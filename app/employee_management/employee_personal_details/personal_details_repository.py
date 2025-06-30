# from typing import List, Optional
# from sqlalchemy import select, update, delete
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from fastapi import status

# from app.models.employee_data.employee_personal_details_model import PersonalDetails
# from app.employee_management.employee_personal_details.personal_details_schema import (
#     PersonalDetailsCreate, 
#     PersonalDetailsUpdate
# )
# from app.core.utilities.exceptions.base import AppException
# from app.core.constants import ResponseMessage, ErrorCode

# # Initialize response messages
# response_message = ResponseMessage()


# class EmployeePersonalDetailsRepository:
#     """
#     Repository class for handling all database operations related to employee personal details.
#     Implements full CRUD operations with proper error handling and validation.
#     """

#     async def create_employee_personal_details(
#         self, 
#         db: AsyncSession, 
#         personal_data: PersonalDetailsCreate
#     ) -> PersonalDetails:
#         """
#         Create new employee personal details after checking for uniqueness.
        
#         Args:
#             db: Database session
#             personal_data: Personal details data to create
            
#         Returns:
#             PersonalDetails: Created personal details object
            
#         Raises:
#             AppException: If employee already has personal details or database error occurs
#         """
#         try:
#             # Check if personal details already exist for this employee
#             existing_details = await self._get_by_employee_id(db, personal_data.employee_id)
            
#             if existing_details:
#                 raise AppException(
#                     message_key=response_message.FORBIDDEN_ACCESS,
#                     details=f"Personal details already exist for employee ID: {personal_data.employee_id}",
#                     status_code=status.HTTP_409_CONFLICT
#                 )
            
#             # Create new personal details
#             new_personal_details = PersonalDetails(**personal_data.model_dump())
#             db.add(new_personal_details)
#             await db.commit()
#             await db.refresh(new_personal_details)
            
#             return new_personal_details
            
#         except IntegrityError as e:
#             await db.rollback()
#             raise AppException(
#                 message_key="INTEGRITY_ERROR",
#                 details=f"Database integrity constraint violated: {str(e)}",
#                 status_code=status.HTTP_400_BAD_REQUEST
#             )
#         except SQLAlchemyError as e:
#             await db.rollback()
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Database operation failed: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def get_employee_personal_details_by_id(
#         self, 
#         db: AsyncSession, 
#         personal_details_id: str
#     ) -> Optional[PersonalDetails]:
#         """
#         Retrieve employee personal details by personal details ID.
        
#         Args:
#             db: Database session
#             personal_details_id: Unique identifier for personal details
            
#         Returns:
#             PersonalDetails or None: Personal details object if found
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             query = select(PersonalDetails).where(
#                 PersonalDetails.employee_personal_details_id == personal_details_id
#             )
#             result = await db.execute(query)
#             return result.scalar_one_or_none()
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to retrieve personal details: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def check_for_new_employee(
#         self, 
#         db: AsyncSession, 
#         employee_id: str
#     ) -> Optional[PersonalDetails]:
#         """
#         Retrieve employee personal details by employee ID.
        
#         Args:
#             db: Database session
#             employee_id: Employee identifier
            
#         Returns:
#             PersonalDetails or None: Personal details object if found
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             return await self._get_by_employee_id(db, employee_id)
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to retrieve personal details for employee: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
    
#     async def get_employee_personal_details_by_employee_id(
#         self, 
#         db: AsyncSession, 
#         employee_id: str
#     ) -> Optional[PersonalDetails]:
#         """
#         Retrieve employee personal details by employee ID.
        
#         Args:
#             db: Database session
#             employee_id: Employee identifier
            
#         Returns:
#             PersonalDetails or None: Personal details object if found
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             return await self._get_by_employee_id(db, employee_id)
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to retrieve personal details for employee: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def get_all_employee_personal_details(
#         self, 
#         db: AsyncSession,
#         skip: int = 0,
#         limit: int = 100
#     ) -> List[PersonalDetails]:
#         """
#         Retrieve all employee personal details with pagination.
        
#         Args:
#             db: Database session
#             skip: Number of records to skip
#             limit: Maximum number of records to return
            
#         Returns:
#             List[PersonalDetails]: List of personal details objects
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             query = select(PersonalDetails).offset(skip).limit(limit)
#             result = await db.execute(query)
#             return result.scalars().all()
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to retrieve personal details list: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )



    
#     async def update_employee_personal_details(
#         self, 
#         db: AsyncSession, 
#         personal_details_id: str,
#         update_data: PersonalDetailsUpdate
#     ) -> Optional[PersonalDetails]:
#         """
#         Update employee personal details.
        
#         Args:
#             db: Database session
#             personal_details_id: Unique identifier for personal details
#             update_data: Data to update
            
#         Returns:
#             PersonalDetails or None: Updated personal details object
            
#         Raises:
#             AppException: If personal details not found or database error occurs
#         """
#         try:
#             # Check if personal details exist
#             existing_details = await self.get_employee_personal_details_by_id(
#                 db, personal_details_id
#             )
            
#             if not existing_details:
#                 raise AppException(
#                     message_key=response_message.RESOURCE_NOT_FOUND,
#                     details=f"Personal details not found with ID: {personal_details_id}",
#                     status_code=status.HTTP_404_NOT_FOUND
#                 )
            
#             # Prepare update data (exclude None values)
#             update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
#             if not update_dict:
#                 # No fields to update
#                 return existing_details
            
#             # Perform update
#             query = (
#                 update(PersonalDetails)
#                 .where(PersonalDetails.employee_personal_details_id == personal_details_id)
#                 .values(**update_dict)
#                 .returning(PersonalDetails)
#             )
            
#             result = await db.execute(query)
#             await db.commit()
            
#             updated_details = result.scalar_one_or_none()
#             if updated_details:
#                 await db.refresh(updated_details)
            
#             return updated_details
            
#         except IntegrityError as e:
#             await db.rollback()
#             raise AppException(
#                 message_key="INTEGRITY_ERROR",
#                 details=f"Database integrity constraint violated: {str(e)}",
#                 status_code=status.HTTP_400_BAD_REQUEST
#             )
#         except SQLAlchemyError as e:
#             await db.rollback()
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to update personal details: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def delete_employee_personal_details(
#         self, 
#         db: AsyncSession, 
#         personal_details_id: str
#     ) -> bool:
#         """
#         Delete employee personal details.
        
#         Args:
#             db: Database session
#             personal_details_id: Unique identifier for personal details
            
#         Returns:
#             bool: True if deletion successful, False if not found
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             # Check if personal details exist
#             existing_details = await self.get_employee_personal_details_by_id(
#                 db, personal_details_id
#             )
            
#             if not existing_details:
#                 raise AppException(
#                     message_key=response_message.RESOURCE_NOT_FOUND,
#                     details=f"Personal details not found with ID: {personal_details_id}",
#                     status_code=status.HTTP_404_NOT_FOUND
#                 )
            
#             # Delete personal details
#             query = delete(PersonalDetails).where(
#                 PersonalDetails.employee_personal_details_id == personal_details_id
#             )
            
#             result = await db.execute(query)
#             await db.commit()
            
#             return result.rowcount > 0
            
#         except SQLAlchemyError as e:
#             await db.rollback()
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to delete personal details: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def search_personal_details(
#         self, 
#         db: AsyncSession,
#         search_term: str,
#         skip: int = 0,
#         limit: int = 100
#     ) -> List[PersonalDetails]:
#         """
#         Search employee personal details by name or email.
        
#         Args:
#             db: Database session
#             search_term: Term to search for
#             skip: Number of records to skip
#             limit: Maximum number of records to return
            
#         Returns:
#             List[PersonalDetails]: List of matching personal details
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             search_pattern = f"%{search_term.lower()}%"
            
#             query = select(PersonalDetails).where(
#                 (PersonalDetails.first_name.ilike(search_pattern)) |
#                 (PersonalDetails.last_name.ilike(search_pattern)) |
#                 (PersonalDetails.personal_email.ilike(search_pattern))
#             ).offset(skip).limit(limit)
            
#             result = await db.execute(query)
#             return result.scalars().all()
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Search operation failed: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     async def get_personal_details_count(self, db: AsyncSession) -> int:
#         """
#         Get total count of personal details records.
        
#         Args:
#             db: Database session
            
#         Returns:
#             int: Total count of records
            
#         Raises:
#             AppException: If database error occurs
#         """
#         try:
#             from sqlalchemy import func
#             query = select(func.count(PersonalDetails.employee_personal_details_id))
#             result = await db.execute(query)
#             return result.scalar_one()
            
#         except SQLAlchemyError as e:
#             raise AppException(
#                 message_key="DB_ERROR",
#                 details=f"Failed to get count: {str(e)}",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     # Private helper methods
#     async def _get_by_employee_id(
#         self, 
#         db: AsyncSession, 
#         employee_id: str
#     ) -> Optional[PersonalDetails]:
#         """
#         Private method to get personal details by employee ID.
        
#         Args:
#             db: Database session
#             employee_id: Employee identifier
            
#         Returns:
#             PersonalDetails or None: Personal details object if found
#         """
#         query = select(PersonalDetails).where(PersonalDetails.employee_id == employee_id)
#         result = await db.execute(query)
#         return result.scalar_one_or_none()







from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import status

from app.models.employee_data.employee_personal_details_model import PersonalDetails
from app.employee_management.employee_personal_details.personal_details_schema import (
    PersonalDetailsCreate, 
    PersonalDetailsUpdate
)
from app.core.utilities.exceptions.base import AppException
from app.core.constants import ResponseMessage, ErrorCode

# Initialize response messages
response_message = ResponseMessage()


class EmployeePersonalDetailsRepository:
    """
    Repository class for handling all database operations related to employee personal details.
    Implements full CRUD operations with proper error handling and validation.
    """

    async def create_employee_personal_details(
        self, 
        db: AsyncSession, 
        personal_data: PersonalDetailsCreate
    ) -> PersonalDetails:
        """
        Create new employee personal details after checking for uniqueness.
        
        Args:
            db: Database session
            personal_data: Personal details data to create
            
        Returns:
            PersonalDetails: Created personal details object
            
        Raises:
            AppException: If employee already has personal details or database error occurs
        """
        try:
            # Check if personal details already exist for this employee
            existing_details = await self._get_by_employee_id(db, personal_data.employee_id)
            
            if existing_details:
                raise AppException(
                    message_key=response_message.FORBIDDEN_ACCESS,
                    details=f"Personal details already exist for employee ID: {personal_data.employee_id}",
                    status_code=status.HTTP_409_CONFLICT
                )
            
            # Create new personal details
            new_personal_details = PersonalDetails(**personal_data.model_dump())
            db.add(new_personal_details)
            await db.commit()
            await db.refresh(new_personal_details)
            
            return new_personal_details
            
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

    async def get_employee_personal_details_by_id(
        self, 
        db: AsyncSession, 
        personal_details_id: str
    ) -> Optional[PersonalDetails]:
        """
        Retrieve employee personal details by personal details ID.
        
        Args:
            db: Database session
            personal_details_id: Unique identifier for personal details
            
        Returns:
            PersonalDetails or None: Personal details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(PersonalDetails).where(
                PersonalDetails.employee_personal_details_id == personal_details_id
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve personal details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def check_for_new_employee(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> Optional[PersonalDetails]:
        """
        Retrieve employee personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            PersonalDetails or None: Personal details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            return await self._get_by_employee_id(db, employee_id)
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve personal details for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_employee_personal_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> Optional[PersonalDetails]:
        """
        Retrieve employee personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            PersonalDetails or None: Personal details object if found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            return await self._get_by_employee_id(db, employee_id)
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve personal details for employee: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[PersonalDetails]: List of personal details objects
            
        Raises:
            AppException: If database error occurs
        """
        try:
            query = select(PersonalDetails).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to retrieve personal details list: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_personal_details(
        self, 
        db: AsyncSession, 
        personal_details_id: str,
        update_data: PersonalDetailsUpdate
    ) -> Optional[PersonalDetails]:
        """
        Update employee personal details.
        
        Args:
            db: Database session
            personal_details_id: Unique identifier for personal details
            update_data: Data to update
            
        Returns:
            PersonalDetails or None: Updated personal details object
            
        Raises:
            AppException: If personal details not found or database error occurs
        """
        try:
            # Check if personal details exist
            existing_details = await self.get_employee_personal_details_by_id(
                db, personal_details_id
            )
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Personal details not found with ID: {personal_details_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_details
            
            # Perform update
            query = (
                update(PersonalDetails)
                .where(PersonalDetails.employee_personal_details_id == personal_details_id)
                .values(**update_dict)
                .returning(PersonalDetails)
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
                details=f"Failed to update personal details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_employee_personal_details_by_employee_id(
        self, 
        db: AsyncSession, 
        employee_id: str,
        update_data: PersonalDetailsUpdate
    ) -> Optional[PersonalDetails]:
        """
        Update employee personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            update_data: Data to update
            
        Returns:
            PersonalDetails or None: Updated personal details object
            
        Raises:
            AppException: If personal details not found or database error occurs
        """
        try:
            # Check if personal details exist for this employee
            existing_details = await self._get_by_employee_id(db, employee_id)
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Personal details not found for employee ID: {employee_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare update data (exclude None values)
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                # No fields to update
                return existing_details
            
            # Perform update
            query = (
                update(PersonalDetails)
                .where(PersonalDetails.employee_id == employee_id)
                .values(**update_dict)
                .returning(PersonalDetails)
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
                details=f"Failed to update personal details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            bool: True if deletion successful, False if not found
            
        Raises:
            AppException: If database error occurs
        """
        try:
            # Check if personal details exist
            existing_details = await self.get_employee_personal_details_by_id(
                db, personal_details_id
            )
            
            if not existing_details:
                raise AppException(
                    message_key=response_message.RESOURCE_NOT_FOUND,
                    details=f"Personal details not found with ID: {personal_details_id}",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Delete personal details
            query = delete(PersonalDetails).where(
                PersonalDetails.employee_personal_details_id == personal_details_id
            )
            
            result = await db.execute(query)
            await db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise AppException(
                message_key="DB_ERROR",
                details=f"Failed to delete personal details: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[PersonalDetails]: List of matching personal details
            
        Raises:
            AppException: If database error occurs
        """
        try:
            search_pattern = f"%{search_term.lower()}%"
            
            query = select(PersonalDetails).where(
                (PersonalDetails.first_name.ilike(search_pattern)) |
                (PersonalDetails.last_name.ilike(search_pattern)) |
                (PersonalDetails.personal_email.ilike(search_pattern))
            ).offset(skip).limit(limit)
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=f"Search operation failed: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_personal_details_count(self, db: AsyncSession) -> int:
        """
        Get total count of personal details records.
        
        Args:
            db: Database session
            
        Returns:
            int: Total count of records
            
        Raises:
            AppException: If database error occurs
        """
        try:
            from sqlalchemy import func
            query = select(func.count(PersonalDetails.employee_personal_details_id))
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
    ) -> Optional[PersonalDetails]:
        """
        Private method to get personal details by employee ID.
        
        Args:
            db: Database session
            employee_id: Employee identifier
            
        Returns:
            PersonalDetails or None: Personal details object if found
        """
        query = select(PersonalDetails).where(PersonalDetails.employee_id == employee_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()