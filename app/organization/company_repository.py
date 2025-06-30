from app.models.organization.company_model import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.organization.company_schema import CompanyCreate, CompanyUpdate
from fastapi import HTTPException, status
from typing import List
from app.core.utilities.exceptions.base import AppException
from app.core.constants import CompanyConstants


# Constants Initialization
company_constants = CompanyConstants()


class CompanyRepository:
    """
    Repository for handling company data operations.
    """

    async def list_companies_repository(self, db: AsyncSession) -> List[Company]:
        """
        Retrieve all available companies from the database.
        """
        try:
            query = select(Company)
            result = await db.execute(query)
            companies = result.scalars().all()
            return companies
        except SQLAlchemyError as e:
            raise HTTPException(
                                    status_code=409,
                                    detail=f"Database query failed while fetching companies: {e}"
                                )
        except Exception as e:
            raise HTTPException(
                                    status_code=409,
                                    detail=f"Unexpected error in CompanyRepository: {str(e)}"
                                )
    
    async def get_company_repository(self, db: AsyncSession, company_id: str) -> Company:
        """
        Retrieve all available companies from the database.
        """
        try:
            # Check if company_code already exists
            query = select(Company).where(Company.company_id == company_id)
            result = await db.execute(query)
            company = result.scalar_one_or_none()
            
            if not company:
                raise AppException(
                    message_key=company_constants.INVALID_COMPANY_ID,
                    details=f"Company with code '{company_id}' not exists.",
                    status_code=404
                )
                
            return company
        
        except SQLAlchemyError as e:
            raise AppException(
                message_key="DB_ERROR",
                details=str(e),
                status_code=500
            )
    
    
    
    async def create_company_repository(self, db: AsyncSession, company_data: CompanyCreate) -> Company:
        """
        Create a new company after checking uniqueness of company_code.
        """
        try:
            # Check if company_code already exists
            query = select(Company).where(Company.company_code == company_data.company_code)
            result = await db.execute(query)
            existing_company = result.scalar_one_or_none()
            
            if existing_company:
                raise AppException(
                    message_key= company_constants.COMPANY_ALREADY_EXISTS,
                    details=f"company_code: {company_data.company_code}",
                    status_code=409
                )
            
            # Create the Company model instance from schema
            new_company = Company(**company_data.dict())
            
            db.add(new_company)
            await db.commit()
            await db.refresh(new_company)
            return new_company
        
        except SQLAlchemyError as e:
            await db.rollback()  # 🔁 Ensure rollback on any DB-level error
            raise AppException(
                message_key="DB_ERROR",
                details=str(e),
                status_code=500
            )
    
    
    
    async def update_company_repository(self, db: AsyncSession, company_data: CompanyUpdate, company_id: str) -> Company:
        """
        Update a company after checking company_id.
        """
        try:
            # Check if company_code already exists
            query = select(Company).where(Company.company_id == company_id)
            result = await db.execute(query)
            existing_company = result.scalar_one_or_none()

            if not existing_company:
                raise HTTPException(
                                    status_code=409,
                                    detail=f"Company with id '{company_id}' does not exist."
                                )
            
            
            # 2️⃣ Update fields
            update_data = company_data.dict(exclude_unset=True)  # use exclude_unset to avoid overwriting with None

            for key, value in update_data.items():
                setattr(existing_company, key, value)
            await db.commit()
            await db.refresh(existing_company)
            return existing_company

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Database error while creating company:  {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Unexpected error in CompanyRepository: {str(e)}"
            )
    
    
    async def delete_company_repository(self, db: AsyncSession, company_id: str) -> str:
        """
        Update a company after checking company_id.
        """
        try:
            # Check if company_code already exists
            query = select(Company).where(Company.company_id == company_id)
            result = await db.execute(query)
            existing_company = result.scalar_one_or_none()

            if not existing_company:
                raise HTTPException(
                                    status_code=409,
                                    detail=f"Company with id '{company_id}' does not exist."
                                )
            
            
            # delete the company
            await db.delete(existing_company)
            await db.commit()
            return f"Company of {company_id} deleted Successfully."

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Database error while creating company:  {e}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Unexpected error in CompanyRepository: {str(e)}"
            )