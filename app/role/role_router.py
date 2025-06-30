from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.role.role_service import RoleService
from app.db.session import get_db
from typing import List
from app.role.role_schema import RoleResponse, RoleCreate, RoleUpdate
from app.tasks.jwt_session import get_current_user
from app.core.utilities.response_helpers import success_response
from app.core.constants import RoleConstants

############################################
# Role constant initialization
############################################
role_constants = RoleConstants()


# Dependency injection (can later allow injecting mock services for testing)
def get_role_service() -> RoleService:
    return RoleService()

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_roles(
    db: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    try:
        roles = await role_service.list_roles_service(db)
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/my", status_code=status.HTTP_200_OK)
async def get_role(
    db: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
    current_user: dict = Depends(get_current_user)
):
    
    role = await role_service.get_role_service(db, current_user['role_id'])
    role_response = RoleResponse.from_orm(role)
    return success_response(role_response, message=role_constants.ROLE_RETRIEVED)

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_create: RoleCreate,
    db: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    try:
        created_role = await role_service.create_role_service(db, role_create)
        return created_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_role(
    role_id: str,
    role_update: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    try:
        updated_role = await role_service.update_role_service(db, role_update, role_id)
        return updated_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{role_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_role(
    role_id: str,
    db: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    try:
        delete_role_message = await role_service.delete_role_service(db, role_id)
        return delete_role_message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
