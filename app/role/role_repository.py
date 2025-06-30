from app.models.organization.role_model import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.role.role_schema import RoleCreate, RoleUpdate
from fastapi import HTTPException, status
from typing import List
from app.core.utilities.exceptions.base import AppException
from app.core.constants import RoleConstants

############################################
# Role constant initialization
############################################
role_constants = RoleConstants()

class RoleRepository:
    """
    Repository for handling role data operations.
    """

    async def list_roles_repository(self, db: AsyncSession) -> List[Role]:
        """
        Retrieve all available roles from the database.
        """
        try:
            query = select(Role)
            result = await db.execute(query)
            roles = result.scalars().all()
            return roles
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=409,
                detail=f"Database query failed while fetching roles: {e}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=409,
                detail=f"Unexpected error in RoleRepository: {str(e)}"
            )

    async def get_role_repository(self, db: AsyncSession, role_id: str) -> Role:
        """
        Retrieve a role by role_id.
        """
        try:
            query = select(Role).where(Role.role_id == role_id)
            result = await db.execute(query)
            role = result.scalar_one_or_none()

            if not role:
                raise AppException(
                    message_key= role_constants.ROLE_NOT_FOUND,
                    details=f"specified role does not exists: {role_id}",
                    status_code=409
                )
            return role

        except SQLAlchemyError as e:
            await db.rollback()  # 🔁 Ensure rollback on any DB-level error
            raise AppException(
                message_key="DB_ERROR",
                details=f"Database query failed while fetching role: {e}",
                status_code=500
            )

    async def create_role_repository(self, db: AsyncSession, role_data: RoleCreate) -> Role:
        """
        Create a new role after checking uniqueness of role_name.
        """
        try:
            # Check if role_name already exists for the same company
            query = select(Role).where(
                (Role.role_name == role_data.role_name) &
                (Role.company_id == role_data.company_id)
            )
            result = await db.execute(query)
            existing_role = result.scalar_one_or_none()

            if existing_role:
                raise HTTPException(
                    status_code=409,
                    detail=f"Role with name '{role_data.role_name}' already exists for this company."
                )
                
            
            new_role = Role(**role_data.dict())
            
            # new_role = Role(
            #     company_id=role_data.company_id,
            #     role_name=role_data.role_name,
            #     role_code=role_data.role_code,
            #     role_description=role_data.role_description,
            #     is_system_role=role_data.is_system_role,
            #     is_active=role_data.is_active,
            #     # ⚠️ All permission fields can be auto filled if you want default False (already set by model defaults)
            #     **role_data.permissions.dict()  # Optional if you split permissions into nested schemas
            # )

            db.add(new_role)
            await db.commit()
            await db.refresh(new_role)
            return new_role

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while creating role: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleRepository: {str(e)}"
            )

    async def update_role_repository(self, db: AsyncSession, role_data: RoleUpdate, role_id: str) -> Role:
        """
        Update a role after checking role_id.
        """
        try:
            query = select(Role).where(Role.role_id == role_id)
            result = await db.execute(query)
            existing_role = result.scalar_one_or_none()

            if not existing_role:
                raise HTTPException(
                    status_code=409,
                    detail=f"Role with id '{role_id}' does not exist."
                )

            update_data = role_data.dict(exclude_unset=True)

            for key, value in update_data.items():
                setattr(existing_role, key, value)

            await db.commit()
            await db.refresh(existing_role)
            return existing_role

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while updating role: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleRepository: {str(e)}"
            )

    async def delete_role_repository(self, db: AsyncSession, role_id: str) -> str:
        """
        Delete a role after checking role_id.
        """
        try:
            query = select(Role).where(Role.role_id == role_id)
            result = await db.execute(query)
            existing_role = result.scalar_one_or_none()

            if not existing_role:
                raise HTTPException(
                    status_code=409,
                    detail=f"Role with id '{role_id}' does not exist."
                )

            await db.delete(existing_role)
            await db.commit()
            return f"Role with id {role_id} deleted successfully."

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error while deleting role: {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleRepository: {str(e)}"
            )
