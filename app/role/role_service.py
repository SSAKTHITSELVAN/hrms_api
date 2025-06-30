from app.role.role_repository import RoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.organization.role_model import Role
from app.role.role_schema import RoleCreate, RoleUpdate
from fastapi import HTTPException, status
from typing import List

class RoleService:

    def __init__(self, repository: RoleRepository = None) -> None:
        self.repository = repository or RoleRepository()

    async def list_roles_service(self, db: AsyncSession) -> List[Role]:
        try:
            roles = await self.repository.list_roles_repository(db)
            return roles
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service failed to retrieve roles from the database: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error while listing roles: {str(e)}"
            )

    async def get_role_service(self, db: AsyncSession, role_id: str) -> Role:
        role = await self.repository.get_role_repository(db, role_id)
        return role

    async def create_role_service(self, db: AsyncSession, role_create: RoleCreate) -> Role:
        try:
            created_role = await self.repository.create_role_repository(db, role_create)
            return created_role
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while creating role: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleService while creating role: {str(e)}"
            )

    async def update_role_service(self, db: AsyncSession, role_update: RoleUpdate, role_id: str) -> Role:
        try:
            updated_role = await self.repository.update_role_repository(db, role_update, role_id)
            return updated_role
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while updating role: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleService while updating role: {str(e)}"
            )

    async def delete_role_service(self, db: AsyncSession, role_id: str) -> str:
        try:
            delete_message = await self.repository.delete_role_repository(db, role_id)
            return delete_message
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service error while deleting role: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected error in RoleService while deleting role: {str(e)}"
            )
