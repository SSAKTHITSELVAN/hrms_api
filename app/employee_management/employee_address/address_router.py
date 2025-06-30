from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_address.address_schema import (
    AddressCreate, 
    AddressUpdate,
    AddressResponse,
    AddressType
)
from app.employee_management.employee_address.address_service import (
    EmployeeAddressService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/address",
    tags=['Employee Address']
)


def get_address_service() -> EmployeeAddressService:
    """
    Dependency injection for address service.
    
    Returns:
        EmployeeAddressService: Service instance
    """
    return EmployeeAddressService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Employee Address",
    description="Create new employee address record (only one address per type allowed)"
)
async def create_employee_address(
    address: AddressCreate,
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new employee address.
    Only one address per type (permanent, current, work) is allowed per employee.
    
    Args:
        address: Address data to create
        service: Address service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with created address
        
    Raises:
        400: If employee already has an address of this type
    """
    address.employee_id = current_user['employee_id']
    created_address = await service.create_employee_address(db, address)
    response_data = AddressResponse.model_validate(created_address)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Address by ID",
    description="Retrieve employee address by address ID"
)
async def get_employee_address_by_id(
    address_id: str = Path(..., description="Address unique identifier"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get employee address by address ID.
    
    Args:
        address_id: Address unique identifier
        service: Address service instance
        db: Database session
        
    Returns:
        Success response with address data
    """
    address = await service.get_employee_address_by_id(db, address_id)
    response_data = AddressResponse.model_validate(address)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get My Addresses",
    description="Retrieve all addresses for the current employee"
)
async def get_my_addresses(
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all addresses for the current employee.
    
    Args:
        service: Address service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with list of addresses
    """
    addresses = await service.get_employee_addresses_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = [AddressResponse.model_validate(addr) for addr in addresses]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Addresses by Employee ID",
    description="Retrieve all addresses for a specific employee"
)
async def get_employee_addresses_by_employee_id(
    employee_id: str = Path(..., description="Employee unique identifier"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    """
    Get all addresses for a specific employee.
    
    Args:
        employee_id: Employee unique identifier
        service: Address service instance
        db: Database session
        
    Returns:
        Success response with list of addresses
    """
    addresses = await service.get_employee_addresses_by_employee_id(db, current_user["employee_id"])
    response_data = [AddressResponse.model_validate(addr) for addr in addresses]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Addresses",
    description="Retrieve all employee addresses with pagination"
)
async def get_all_employee_addresses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all employee addresses with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Address service instance
        db: Database session
        
    Returns:
        Success response with list of addresses and metadata
    """
    addresses_list = await service.get_all_employee_addresses(db, skip, limit)
    total_count = await service.get_addresses_count(db)
    
    response_data = {
        "items": [AddressResponse.model_validate(item) for item in addresses_list],
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
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Address by ID",
    description="Update employee address by address ID"
)
async def update_employee_address(
    update_data: AddressUpdate,
    address_id: str = Path(..., description="Address unique identifier"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Update employee address by address ID.
    
    Args:
        update_data: Data to update
        address_id: Address unique identifier
        service: Address service instance
        db: Database session
        
    Returns:
        Success response with updated address
    """
    updated_address = await service.update_employee_address(
        db, address_id, update_data
    )
    response_data = AddressResponse.model_validate(updated_address)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )



@router.put(
    "/my/type/{address_type}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update My Address by Type",
    description="Update current user's address by address type"
)
async def update_my_address_by_type(
    update_data: AddressUpdate,
    address_type: AddressType = Path(..., description="Type of address to update"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's address by address type.
    This allows users to update their own addresses by type.
    
    Args:
        update_data: Data to update
        address_type: Type of address (permanent, current, work)
        service: Address service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with updated address
        
    Raises:
        404: If no address of the specified type exists for the current user
        400: If trying to change address_type to one that already exists
    """
    # print("--------------------posted===>", update_data)
    updated_address = await service.update_employee_address_by_employee_id(
        db, current_user['employee_id'], address_type, update_data
    )
    # print("----------------############----after process===>", update_data)
    response_data = AddressResponse.model_validate(updated_address)
    
    return success_response(
        data=response_data,
        message=f"Your {address_type.value} address updated successfully",
        code=status.HTTP_200_OK
    )

@router.get(
    "/my/check/{address_type}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update My Address by Type",
    description="Update current user's address by address type"
)
async def check_my_address_by_type(
    address_type: AddressType = Path(..., description="Type of address to update"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's address by address type.
    This allows users to update their own addresses by type.
    
    Args:
        update_data: Data to update
        address_type: Type of address (permanent, current, work)
        service: Address service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with updated address
        
    Raises:
        404: If no address of the specified type exists for the current user
        400: If trying to change address_type to one that already exists
    """
    updated_address = await service.check_employee_address_by_employee_id(
        db, current_user['employee_id'], address_type,
    )
    response_data = (updated_address)
    
    return success_response(
        data=response_data,
        message=f"Your {address_type.value} address updated successfully",
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Address",
    description="Delete employee address by ID"
)
async def delete_employee_address(
    address_id: str = Path(..., description="Address unique identifier"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete employee address.
    
    Args:
        address_id: Address unique identifier
        service: Address service instance
        db: Database session
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_employee_address(db, address_id)
    
    return success_response(
        data={"deleted": True, "address_id": address_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/type/{address_type}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Addresses by Type",
    description="Get current employee's addresses by type"
)
async def get_addresses_by_type(
    address_type: AddressType = Path(..., description="Type of address"),
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get current employee's addresses by type.
    
    Args:
        address_type: Type of address (permanent, current, work)
        service: Address service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with matching addresses
    """
    addresses = await service.get_addresses_by_type(
        db, current_user['employee_id'], address_type
    )
    response_data = [AddressResponse.model_validate(addr) for addr in addresses]
    
    return success_response(
        data=response_data,
        message=f"Addresses of type '{address_type}' retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/stats/count",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Address Count",
    description="Get total count of address records"
)
async def get_addresses_count(
    service: EmployeeAddressService = Depends(get_address_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get total count of address records.
    
    Args:
        service: Address service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_addresses_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )