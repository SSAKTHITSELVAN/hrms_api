from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_family_details.family_details_schema import (
    FamilyDetailsCreate, 
    FamilyDetailsUpdate,
    FamilyDetailsResponse
)
from app.employee_management.employee_family_details.family_details_service import (
    EmployeeFamilyDetailsService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/family_details",
    tags=['Employee Family Details']
)


def get_family_details_service() -> EmployeeFamilyDetailsService:
    """
    Dependency injection for family details service.
    
    Returns:
        EmployeeFamilyDetailsService: Service instance
    """
    return EmployeeFamilyDetailsService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Employee Family Details",
    description="Create new employee family details record"
)
async def create_employee_family_details(
    family_details: FamilyDetailsCreate,
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new employee family details.
    
    Args:
        family_details: Family details data to create
        service: Family details service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with created family details
    """
    family_details.employee_id = current_user['employee_id']
    created_details = await service.create_employee_family_details(db, family_details)
    response_data = FamilyDetailsResponse.model_validate(created_details)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{family_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Family Details by ID",
    description="Retrieve employee family details by family details ID"
)
async def get_employee_family_details_by_id(
    family_details_id: str = Path(..., description="Family details unique identifier"),
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get employee family details by family details ID.
    
    Args:
        family_details_id: Family details unique identifier
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response with family details data
    """
    family_details = await service.get_employee_family_details_by_id(
        db, family_details_id
    )
    response_data = FamilyDetailsResponse.model_validate(family_details)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/check",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Check Family Details by Employee ID",
    description="Check if employee has family details"
)
async def check_for_new_employee(
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Check if employee has family details.
    
    Args:
        service: Family details service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with check result
    """
    family_details = await service.check_for_new_employee(
        db, current_user['employee_id']
    )
    response_data = family_details
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Family Details",
    description="Retrieve employee family details for current user"
)
async def get_employee_family_details_by_employee_id(
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get employee family details for current user.
    
    Args:
        service: Family details service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with family details data
    """
    family_details = await service.get_employee_family_details_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = FamilyDetailsResponse.model_validate(family_details)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Family Details",
    description="Retrieve all employee family details with pagination"
)
async def get_all_employee_family_details(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all employee family details with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response with list of family details and metadata
    """
    family_details_list = await service.get_all_employee_family_details(db, skip, limit)
    total_count = await service.get_family_details_count(db)
    
    response_data = {
        "items": [FamilyDetailsResponse.model_validate(item) for item in family_details_list],
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
    "/{family_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Family Details",
    description="Update employee family details by ID"
)
async def update_employee_family_details(
    update_data: FamilyDetailsUpdate,
    family_details_id: str = Path(..., description="Family details unique identifier"),
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Update employee family details.
    
    Args:
        update_data: Data to update
        family_details_id: Family details unique identifier
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response with updated family details
    """
    updated_details = await service.update_employee_family_details(
        db, family_details_id, update_data
    )
    response_data = FamilyDetailsResponse.model_validate(updated_details)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.put(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update My Family Details",
    description="Update employee family details for current user"
)
async def update_employee_family_details_by_employee_id(
    update_data: FamilyDetailsUpdate,
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update employee family details for current user.
    
    Args:
        update_data: Data to update
        service: Family details service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with updated family details
    """
    updated_details = await service.update_employee_family_details_by_employee_id(
        db, current_user['employee_id'], update_data
    )
    response_data = FamilyDetailsResponse.model_validate(updated_details)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{family_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Family Details",
    description="Delete employee family details by ID"
)
async def delete_employee_family_details(
    family_details_id: str = Path(..., description="Family details unique identifier"),
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete employee family details.
    
    Args:
        family_details_id: Family details unique identifier
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_employee_family_details(db, family_details_id)
    
    return success_response(
        data={"deleted": True, "family_details_id": family_details_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Search Family Details",
    description="Search employee family details by family member names"
)
async def search_family_details(
    q: str = Query(..., min_length=2, description="Search term (family member name)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Search employee family details by family member names.
    
    Args:
        q: Search term (minimum 2 characters)
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response with search results
    """
    search_results = await service.search_family_details(db, q, skip, limit)
    
    response_data = {
        "items": [FamilyDetailsResponse.model_validate(item) for item in search_results],
        "search_term": q,
        "count": len(search_results),
        "skip": skip,
        "limit": limit
    }
    
    return success_response(
        data=response_data,
        message=f"Search completed for term: '{q}'",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Family Details Count",
    description="Get total count of family details records"
)
async def get_family_details_count(
    service: EmployeeFamilyDetailsService = Depends(get_family_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get total count of family details records.
    
    Args:
        service: Family details service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_family_details_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )