# from typing import List
# from fastapi import APIRouter, status, Depends, Query, Path
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.employee_management.employee_personal_details.personal_details_schema import (
#     PersonalDetailsCreate, 
#     PersonalDetailsUpdate,
#     PersonalDetailsResponse
# )
# from app.employee_management.employee_personal_details.personal_details_service import (
#     EmployeePersonalDetailsService
# )
# from app.db.session import get_db
# from app.core.utilities.response_helpers import success_response
# from app.core.constants import ResponseMessage
# from app.tasks.jwt_session import get_current_user

# # Initialize response messages
# response_message = ResponseMessage()

# # Router configuration
# router = APIRouter(
#     prefix="/personal_details",
#     tags=['Employee Personal Details']
# )


# def get_personal_details_service() -> EmployeePersonalDetailsService:
#     """
#     Dependency injection for personal details service.
    
#     Returns:
#         EmployeePersonalDetailsService: Service instance
#     """
#     return EmployeePersonalDetailsService()


# @router.post(
#     "/", 
#     status_code=status.HTTP_201_CREATED,
#     response_model=dict,
#     summary="Create Employee Personal Details",
#     description="Create new employee personal details record"
# )
# async def create_employee_personal_details(
#     personal_details: PersonalDetailsCreate,
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """
#     Create new employee personal details.
    
#     Args:
#         personal_details: Personal details data to create
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with created personal details
#     """
#     # print("------------------====b==----->", personal_details)
#     personal_details.employee_id = current_user['employee_id']
#     created_details = await service.create_employee_personal_details(db, personal_details)
#     response_data = PersonalDetailsResponse.model_validate(created_details)
    
#     return success_response(
#         data=response_data, 
#         message=response_message.CREATED_SUCCESS, 
#         code=status.HTTP_201_CREATED
#     )


# @router.get(
#     "/{personal_details_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Get Personal Details by ID",
#     description="Retrieve employee personal details by personal details ID"
# )
# async def get_employee_personal_details_by_id(
#     personal_details_id: str = Path(..., description="Personal details unique identifier"),
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Get employee personal details by personal details ID.
    
#     Args:
#         personal_details_id: Personal details unique identifier
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with personal details data
#     """
#     print("----------------------------------------wooo--------")
#     personal_details = await service.get_employee_personal_details_by_id(
#         db, personal_details_id
#     )
#     response_data = PersonalDetailsResponse.model_validate(personal_details)
    
#     return success_response(
#         data=response_data,
#         message=response_message.SUCCESS,
#         code=status.HTTP_200_OK
#     )


# @router.get(
#     "/employee/check",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Get Personal Details by Employee ID",
#     description="Retrieve employee personal details by employee ID"
# )


# async def check_for_new_employee(
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """
#     Get employee personal details by employee ID.
    
#     Args:
#         employee_id: Employee unique identifier
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with personal details data
#     """
#     personal_details = await service.check_for_new_employee(
#         db, current_user['employee_id']
#     )
#     response_data = (personal_details)
    
#     return success_response(
#         data=response_data,
#         message=response_message.SUCCESS,
#         code=status.HTTP_200_OK
#     )



# @router.get(
#     "/employee/my",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Get Personal Details by Employee ID",
#     description="Retrieve employee personal details by employee ID"
# )
# async def get_employee_personal_details_by_employee_id(
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """
#     Get employee personal details by employee ID.
    
#     Args:
#         employee_id: Employee unique identifier
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with personal details data
#     """
#     personal_details = await service.get_employee_personal_details_by_employee_id(
#         db, current_user['employee_id']
#     )
#     response_data = PersonalDetailsResponse.model_validate(personal_details)
    
#     return success_response(
#         data=response_data,
#         message=response_message.SUCCESS,
#         code=status.HTTP_200_OK
#     )

# @router.get(
#     "/",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Get All Personal Details",
#     description="Retrieve all employee personal details with pagination"
# )
# async def get_all_employee_personal_details(
#     skip: int = Query(0, ge=0, description="Number of records to skip"),
#     limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Get all employee personal details with pagination.
    
#     Args:
#         skip: Number of records to skip
#         limit: Maximum number of records to return
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with list of personal details and metadata
#     """
#     print("------------------------------------------this black hat------------")
#     personal_details_list = await service.get_all_employee_personal_details(db, skip, limit)
#     total_count = await service.get_personal_details_count(db)
    
#     response_data = {
#         "items": [PersonalDetailsResponse.model_validate(item) for item in personal_details_list],
#         "total": total_count,
#         "skip": skip,
#         "limit": limit,
#         "has_more": (skip + limit) < total_count
#     }
    
#     return success_response(
#         data=response_data,
#         message=response_message.SUCCESS,
#         code=status.HTTP_200_OK
#     )


# @router.put(
#     "/{personal_details_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Update Personal Details",
#     description="Update employee personal details by ID"
# )
# async def update_employee_personal_details(
#     update_data: PersonalDetailsUpdate,
#     personal_details_id: str = Path(..., description="Personal details unique identifier"),
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Update employee personal details.
    
#     Args:
#         update_data: Data to update
#         personal_details_id: Personal details unique identifier
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with updated personal details
#     """
#     updated_details = await service.update_employee_personal_details(
#         db, personal_details_id, update_data
#     )
#     response_data = PersonalDetailsResponse.model_validate(updated_details)
    
#     return success_response(
#         data=response_data,
#         message=response_message.UPDATED_SUCCESS,
#         code=status.HTTP_200_OK
#     )


# @router.delete(
#     "/{personal_details_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Delete Personal Details",
#     description="Delete employee personal details by ID"
# )
# async def delete_employee_personal_details(
#     personal_details_id: str = Path(..., description="Personal details unique identifier"),
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Delete employee personal details.
    
#     Args:
#         personal_details_id: Personal details unique identifier
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response confirming deletion
#     """
#     await service.delete_employee_personal_details(db, personal_details_id)
    
#     return success_response(
#         data={"deleted": True, "personal_details_id": personal_details_id},
#         message=response_message.DELETED_SUCCESS,
#         code=status.HTTP_200_OK
#     )


# @router.get(
#     "/search/",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Search Personal Details",
#     description="Search employee personal details by name or email"
# )
# async def search_personal_details(
#     q: str = Query(..., min_length=2, description="Search term (name or email)"),
#     skip: int = Query(0, ge=0, description="Number of records to skip"),
#     limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Search employee personal details by name or email.
    
#     Args:
#         q: Search term (minimum 2 characters)
#         skip: Number of records to skip
#         limit: Maximum number of records to return
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with search results
#     """
#     search_results = await service.search_personal_details(db, q, skip, limit)
    
#     response_data = {
#         "items": [PersonalDetailsResponse.model_validate(item) for item in search_results],
#         "search_term": q,
#         "count": len(search_results),
#         "skip": skip,
#         "limit": limit
#     }
    
#     return success_response(
#         data=response_data,
#         message=f"Search completed for term: '{q}'",
#         code=status.HTTP_200_OK
#     )


# @router.get(
#     "/stats/count",
#     status_code=status.HTTP_200_OK,
#     response_model=dict,
#     summary="Get Personal Details Count",
#     description="Get total count of personal details records"
# )
# async def get_personal_details_count(
#     service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Get total count of personal details records.
    
#     Args:
#         service: Personal details service instance
#         db: Database session
        
#     Returns:
#         Success response with count information
#     """
#     total_count = await service.get_personal_details_count(db)
    
#     return success_response(
#         data={"total_records": total_count},
#         message="Count retrieved successfully",
#         code=status.HTTP_200_OK
#     )



from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_personal_details.personal_details_schema import (
    PersonalDetailsCreate, 
    PersonalDetailsUpdate,
    PersonalDetailsResponse
)
from app.employee_management.employee_personal_details.personal_details_service import (
    EmployeePersonalDetailsService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/personal_details",
    tags=['Employee Personal Details']
)


def get_personal_details_service() -> EmployeePersonalDetailsService:
    """
    Dependency injection for personal details service.
    
    Returns:
        EmployeePersonalDetailsService: Service instance
    """
    return EmployeePersonalDetailsService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Employee Personal Details",
    description="Create new employee personal details record"
)
async def create_employee_personal_details(
    personal_details: PersonalDetailsCreate,
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new employee personal details.
    
    Args:
        personal_details: Personal details data to create
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with created personal details
    """
    # print("------------------====b==----->", personal_details)
    personal_details.employee_id = current_user['employee_id']
    created_details = await service.create_employee_personal_details(db, personal_details)
    response_data = PersonalDetailsResponse.model_validate(created_details)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{personal_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Personal Details by ID",
    description="Retrieve employee personal details by personal details ID"
)
async def get_employee_personal_details_by_id(
    personal_details_id: str = Path(..., description="Personal details unique identifier"),
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get employee personal details by personal details ID.
    
    Args:
        personal_details_id: Personal details unique identifier
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with personal details data
    """
    print("----------------------------------------wooo--------")
    personal_details = await service.get_employee_personal_details_by_id(
        db, personal_details_id
    )
    response_data = PersonalDetailsResponse.model_validate(personal_details)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/check",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Personal Details by Employee ID",
    description="Retrieve employee personal details by employee ID"
)


async def check_for_new_employee(
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get employee personal details by employee ID.
    
    Args:
        employee_id: Employee unique identifier
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with personal details data
    """
    personal_details = await service.check_for_new_employee(
        db, current_user['employee_id']
    )
    response_data = (personal_details)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )



@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Personal Details by Employee ID",
    description="Retrieve employee personal details by employee ID"
)
async def get_employee_personal_details_by_employee_id(
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get employee personal details by employee ID.
    
    Args:
        employee_id: Employee unique identifier
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with personal details data
    """
    personal_details = await service.get_employee_personal_details_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = PersonalDetailsResponse.model_validate(personal_details)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Personal Details",
    description="Retrieve all employee personal details with pagination"
)
async def get_all_employee_personal_details(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all employee personal details with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with list of personal details and metadata
    """
    print("------------------------------------------this black hat------------")
    personal_details_list = await service.get_all_employee_personal_details(db, skip, limit)
    total_count = await service.get_personal_details_count(db)
    
    response_data = {
        "items": [PersonalDetailsResponse.model_validate(item) for item in personal_details_list],
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
    "/{personal_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Personal Details",
    description="Update employee personal details by ID"
)
async def update_employee_personal_details(
    update_data: PersonalDetailsUpdate,
    personal_details_id: str = Path(..., description="Personal details unique identifier"),
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Update employee personal details.
    
    Args:
        update_data: Data to update
        personal_details_id: Personal details unique identifier
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with updated personal details
    """
    updated_details = await service.update_employee_personal_details(
        db, personal_details_id, update_data
    )
    response_data = PersonalDetailsResponse.model_validate(updated_details)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.put(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Personal Details by Employee ID",
    description="Update employee personal details by employee ID"
)
async def update_employee_personal_details_by_employee_id(
    update_data: PersonalDetailsUpdate,
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update employee personal details by employee ID.
    
    Args:
        update_data: Data to update
        service: Personal details service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with updated personal details
    """
    updated_details = await service.update_employee_personal_details_by_employee_id(
        db, current_user['employee_id'], update_data
    )
    response_data = PersonalDetailsResponse.model_validate(updated_details)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{personal_details_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Personal Details",
    description="Delete employee personal details by ID"
)
async def delete_employee_personal_details(
    personal_details_id: str = Path(..., description="Personal details unique identifier"),
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete employee personal details.
    
    Args:
        personal_details_id: Personal details unique identifier
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_employee_personal_details(db, personal_details_id)
    
    return success_response(
        data={"deleted": True, "personal_details_id": personal_details_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Search Personal Details",
    description="Search employee personal details by name or email"
)
async def search_personal_details(
    q: str = Query(..., min_length=2, description="Search term (name or email)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Search employee personal details by name or email.
    
    Args:
        q: Search term (minimum 2 characters)
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with search results
    """
    search_results = await service.search_personal_details(db, q, skip, limit)
    
    response_data = {
        "items": [PersonalDetailsResponse.model_validate(item) for item in search_results],
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
    summary="Get Personal Details Count",
    description="Get total count of personal details records"
)
async def get_personal_details_count(
    service: EmployeePersonalDetailsService = Depends(get_personal_details_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get total count of personal details records.
    
    Args:
        service: Personal details service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_personal_details_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )