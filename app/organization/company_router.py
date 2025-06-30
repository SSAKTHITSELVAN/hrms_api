from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.organization.company_service import CompanyService
from app.db.session import get_db
from typing import List
from app.organization.company_schema import CompanyResponse, CompanyCreate, CompanyUpdate
from app.core.utilities.response_helpers import success_response, error_response
from app.core.constants import CompanyConstants
from app.tasks.jwt_session import get_current_user


# Constants Initialization
company_constants = CompanyConstants()

# Dependency injection (can later allow injecting mock services for testing)
def get_company_service() -> CompanyService:
    return CompanyService()

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_companies(
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(get_company_service)
):
    try:
        companies = await company_service.list_companies_service(db)
        return companies

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/my", status_code=status.HTTP_200_OK)
async def get_company(
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(get_company_service),
    current_user: dict = Depends(get_current_user)
):
    company = await company_service.get_company_service(db, current_user['company_id'])
    company_response = CompanyResponse.from_orm(company)
    return success_response(company_response, message=company_constants.COMPANY_RETRIEVED, code=200)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    company_create: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(get_company_service)
):
    
    created_company = await company_service.create_company_service(db, company_create)
    company_response = CompanyResponse.from_orm(created_company)
    return success_response(company_response, message=company_constants.COMPANY_CREATED)
    

@router.put("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_company(
    company_id: str,
    company_update: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(get_company_service)
):
    try:
        created_company = await company_service.update_company_service(db, company_update, company_id)
        return created_company
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{company_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_company(
    company_id: str,
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(get_company_service)
):
    try:
        delete_company_message = await company_service.delete_company_service(db, company_id)
        return delete_company_message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )