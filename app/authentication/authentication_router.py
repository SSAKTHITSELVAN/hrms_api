from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.authentication.authentication_service import AuthEmployeeSerive
from app.authentication.authentication_schema import EmployeeResponse, EmployeeCreate
from typing import List

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_auth_employee_service() -> AuthEmployeeSerive:
    return AuthEmployeeSerive()

@router.get("/", response_model=List[EmployeeResponse], status_code=status.HTTP_200_OK)
async def list_all_employees(
    employee_service: AuthEmployeeSerive = Depends(get_auth_employee_service),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        employees = await employee_service.list_employees_service(db)
        return employees

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_create: EmployeeCreate,
    employee_service: AuthEmployeeSerive = Depends(get_auth_employee_service),
    db: AsyncSession = Depends(get_db)
    ):
        created_employee = await employee_service.create_employee_service(db, employee_create)
        return created_employee