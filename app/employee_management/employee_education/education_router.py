from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_education.education_schema import (
    EducationCreate, 
    EducationUpdate,
    EducationResponse
)
from app.employee_management.employee_education.education_service import (
    EmployeeEducationService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/education",
    tags=['Employee Education']
)


def get_education_service() -> EmployeeEducationService:
    """
    Dependency injection for education service.
    
    Returns:
        EmployeeEducationService: Service instance
    """
    return EmployeeEducationService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Employee Education",
    description="Create new employee education record"
)
async def create_employee_education(
    education: EducationCreate,
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new employee education record.
    
    Args:
        education: Education data to create
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with created education record
    """
    education.employee_id = current_user['employee_id']
    created_education = await service.create_employee_education(db, education)
    response_data = EducationResponse.model_validate(created_education)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{education_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Education by ID",
    description="Retrieve employee education record by education ID"
)
async def get_employee_education_by_id(
    education_id: str = Path(..., description="Education unique identifier"),
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get employee education record by education ID.
    
    Args:
        education_id: Education unique identifier
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with education data
    """
    education = await service.get_employee_education_by_id(db, education_id)
    response_data = EducationResponse.model_validate(education)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Education Records",
    description="Retrieve all education records for the current employee"
)
async def get_my_education_records(
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all education records for the current employee.
    
    Args:
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with list of education records
    """
    education_records = await service.get_employee_education_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = [EducationResponse.model_validate(record) for record in education_records]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Education Records",
    description="Retrieve all employee education records with pagination"
)
async def get_all_employee_education(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all employee education records with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with list of education records and metadata
    """
    education_list = await service.get_all_employee_education(db, skip, limit)
    total_count = await service.get_education_count(db)
    
    response_data = {
        "items": [EducationResponse.model_validate(item) for item in education_list],
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total_count
    }
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.put(
    "/{education_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Education by ID",
    description="Update employee education record by education ID"
)
async def update_employee_education(
    update_data: EducationUpdate,
    education_id: str = Path(..., description="Education unique identifier"),
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update employee education record by education ID.
    
    Args:
        update_data: Data to update
        education_id: Education unique identifier
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with updated education record
    """
    updated_education = await service.update_employee_education(
        db, education_id, update_data
    )
    response_data = EducationResponse.model_validate(updated_education)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Education Record",
    description="Delete employee education record by ID"
)
async def delete_employee_education(
    education_id: str = Path(..., description="Education unique identifier"),
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete employee education record.
    
    Args:
        education_id: Education unique identifier
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_employee_education(db, education_id)
    
    return success_response(
        data={"deleted": True, "education_id": education_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my/highest",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Highest Qualifications",
    description="Get education records marked as highest qualification for current employee"
)
async def get_my_highest_qualifications(
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get education records marked as highest qualification for current employee.
    
    Args:
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with highest qualification records
    """
    highest_qualifications = await service.get_highest_qualifications(
        db, current_user['employee_id']
    )
    response_data = [EducationResponse.model_validate(record) for record in highest_qualifications]
    
    return success_response(
        data=response_data,
        message="Highest qualifications retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Education Count",
    description="Get total count of education records"
)
async def get_education_count(
    service: EmployeeEducationService = Depends(get_education_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get total count of education records.
    
    Args:
        service: Education service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_education_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )