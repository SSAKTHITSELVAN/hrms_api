from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_work_experience.work_experience_schema import (
    WorkExperienceCreate, 
    WorkExperienceUpdate,
    WorkExperienceResponse
)
from app.employee_management.employee_work_experience.work_experience_service import (
    EmployeeWorkExperienceService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/work_experience",
    tags=['Employee Work Experience']
)


def get_work_experience_service() -> EmployeeWorkExperienceService:
    """
    Dependency injection for work experience service.
    
    Returns:
        EmployeeWorkExperienceService: Service instance
    """
    return EmployeeWorkExperienceService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Employee Work Experience",
    description="Create new employee work experience record"
)
async def create_employee_work_experience(
    work_experience: WorkExperienceCreate,
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new employee work experience.
    
    Args:
        work_experience: Work experience data to create
        service: Work experience service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with created work experience
    """
    work_experience.employee_id = current_user['employee_id']
    created_experience = await service.create_employee_work_experience(db, work_experience)
    response_data = WorkExperienceResponse.model_validate(created_experience)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{experience_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Work Experience by ID",
    description="Retrieve employee work experience by experience ID"
)
async def get_employee_work_experience_by_id(
    experience_id: str = Path(..., description="Work experience unique identifier"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get employee work experience by experience ID.
    
    Args:
        experience_id: Work experience unique identifier
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with work experience data
    """
    work_experience = await service.get_employee_work_experience_by_id(
        db, experience_id
    )
    response_data = WorkExperienceResponse.model_validate(work_experience)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Work Experiences",
    description="Retrieve all work experiences for the current employee"
)
async def get_my_work_experiences(
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all work experiences for the current employee.
    
    Args:
        service: Work experience service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with list of work experiences
    """
    work_experiences = await service.get_employee_work_experiences_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = [WorkExperienceResponse.model_validate(exp) for exp in work_experiences]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/{employee_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Work Experiences by Employee ID",
    description="Retrieve all work experiences for a specific employee"
)
async def get_work_experiences_by_employee_id(
    employee_id: str = Path(..., description="Employee unique identifier"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all work experiences for a specific employee.
    
    Args:
        employee_id: Employee unique identifier
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with list of work experiences
    """
    work_experiences = await service.get_employee_work_experiences_by_employee_id(
        db, employee_id
    )
    response_data = [WorkExperienceResponse.model_validate(exp) for exp in work_experiences]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Work Experiences",
    description="Retrieve all employee work experiences with pagination"
)
async def get_all_employee_work_experiences(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all employee work experiences with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with list of work experiences and metadata
    """
    work_experiences_list = await service.get_all_employee_work_experiences(db, skip, limit)
    total_count = await service.get_work_experience_count(db)
    
    response_data = {
        "items": [WorkExperienceResponse.model_validate(item) for item in work_experiences_list],
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
    "/{experience_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Work Experience",
    description="Update employee work experience by ID"
)
async def update_employee_work_experience(
    update_data: WorkExperienceUpdate,
    experience_id: str = Path(..., description="Work experience unique identifier"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Update employee work experience.
    
    Args:
        update_data: Data to update
        experience_id: Work experience unique identifier
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with updated work experience
    """
    updated_experience = await service.update_employee_work_experience(
        db, experience_id, update_data
    )
    response_data = WorkExperienceResponse.model_validate(updated_experience)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Work Experience",
    description="Delete employee work experience by ID"
)
async def delete_employee_work_experience(
    experience_id: str = Path(..., description="Work experience unique identifier"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete employee work experience.
    
    Args:
        experience_id: Work experience unique identifier
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_employee_work_experience(db, experience_id)
    
    return success_response(
        data={"deleted": True, "experience_id": experience_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Search Work Experiences",
    description="Search employee work experiences by company name, job title, or location"
)
async def search_work_experiences(
    q: str = Query(..., min_length=2, description="Search term (company, job title, or location)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Search employee work experiences by company name, job title, or location.
    
    Args:
        q: Search term (minimum 2 characters)
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with search results
    """
    search_results = await service.search_work_experiences(db, q, skip, limit)
    
    response_data = {
        "items": [WorkExperienceResponse.model_validate(item) for item in search_results],
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
    "/current/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Current Work Experiences",
    description="Get all current work experiences (where end_date is null)"
)
async def get_current_work_experiences(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all current work experiences (where end_date is null).
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with list of current work experiences
    """
    current_experiences = await service.get_current_work_experiences(db, skip, limit)
    
    response_data = {
        "items": [WorkExperienceResponse.model_validate(item) for item in current_experiences],
        "count": len(current_experiences),
        "skip": skip,
        "limit": limit
    }
    
    return success_response(
        data=response_data,
        message="Current work experiences retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Work Experience Count",
    description="Get total count of work experience records"
)
async def get_work_experience_count(
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get total count of work experience records.
    
    Args:
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_work_experience_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count/employee/{employee_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Work Experience Count by Employee",
    description="Get count of work experience records for a specific employee"
)
async def get_work_experience_count_by_employee(
    employee_id: str = Path(..., description="Employee unique identifier"),
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get count of work experience records for a specific employee.
    
    Args:
        employee_id: Employee unique identifier
        service: Work experience service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    count = await service.get_work_experience_count_by_employee(db, employee_id)
    
    return success_response(
        data={"employee_id": employee_id, "work_experience_count": count},
        message="Employee work experience count retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Work Experience Count",
    description="Get count of work experience records for the current employee"
)
async def get_my_work_experience_count(
    service: EmployeeWorkExperienceService = Depends(get_work_experience_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get count of work experience records for the current employee.
    
    Args:
        service: Work experience service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_work_experience_count_by_employee(db)

    return success_response(
        data={"total_records": total_count},
        message="My work experience count retrieved successfully",
        code=status.HTTP_200_OK
    )