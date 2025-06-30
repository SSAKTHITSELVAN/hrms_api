from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.department.department_service import DepartmentService
from app.db.session import get_db
from typing import List
from app.department.department_schema import DepartmentResponse, DepartmentCreate, DepartmentUpdate
# from app.api.response_helpers import success_response, error_response

# Dependency injection (can later allow injecting mock services for testing)
def get_department_service() -> DepartmentService:
    return DepartmentService()

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_departments(
    db: AsyncSession = Depends(get_db),
    department_service: DepartmentService = Depends(get_department_service)
):
    try:
        departments = await department_service.list_departments_service(db)
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{department_id}", response_model=DepartmentResponse, status_code=status.HTTP_200_OK)
async def get_department(
    department_id: str,
    db: AsyncSession = Depends(get_db),
    department_service: DepartmentService = Depends(get_department_service)
):
    try:
        department = await department_service.get_department_service(db, department_id)
        return department
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_create: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    department_service: DepartmentService = Depends(get_department_service)
):
    try:
        created_department = await department_service.create_department_service(db, department_create)
        return created_department
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{department_id}", response_model=DepartmentResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_department(
    department_id: str,
    department_update: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    department_service: DepartmentService = Depends(get_department_service)
):
    try:
        updated_department = await department_service.update_department_service(db, department_update, department_id)
        return updated_department
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{department_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_department(
    department_id: str,
    db: AsyncSession = Depends(get_db),
    department_service: DepartmentService = Depends(get_department_service)
):
    try:
        delete_message = await department_service.delete_department_service(db, department_id)
        return delete_message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
