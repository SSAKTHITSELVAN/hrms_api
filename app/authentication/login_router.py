from fastapi import APIRouter, Depends, HTTPException, status
from app.models.authentication.auth_employee import Employee
from app.db.session import get_db
from app.authentication.login_schema import LoginRequest, LoginResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.jwt_utils import create_access_token
from app.core.security import verify_password
from app.core.utilities.response_helpers import success_response

from app.core.constants import AuthConstants

# Authentication Constants
authentication_constants = AuthConstants()

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

from sqlalchemy import select

@router.post("")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Employee).where(Employee.employee_code == request.employee_code)
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()

    if not employee:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(request.password, employee.employee_hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Prepare token payload
    token_data = {
        "employee_id": str(employee.employee_id),
        "company_id": str(employee.company_id),
        "role_id": str(employee.employee_role_id),
        "department_id": str(employee.employee_department_id)
    }

    access_token = create_access_token(token_data)
    
    login_response = LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )
    
    return success_response(
        data=login_response,
        message= authentication_constants.LOGIN_SUCCESS
    )
