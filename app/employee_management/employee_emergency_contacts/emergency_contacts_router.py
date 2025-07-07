from typing import List
from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.employee_management.employee_emergency_contacts.emergency_contacts_schema import (
    EmergencyContactCreate, 
    EmergencyContactUpdate,
    EmergencyContactResponse
)
from app.employee_management.employee_emergency_contacts.emergency_contacts_service import (
    EmergencyContactService
)
from app.db.session import get_db
from app.core.utilities.response_helpers import success_response
from app.core.constants import ResponseMessage
from app.tasks.jwt_session import get_current_user

# Initialize response messages
response_message = ResponseMessage()

# Router configuration
router = APIRouter(
    prefix="/emergency_contacts",
    tags=['Employee Emergency Contacts']
)


def get_emergency_contacts_service() -> EmergencyContactService:
    """
    Dependency injection for emergency contacts service.
    
    Returns:
        EmergencyContactService: Service instance
    """
    return EmergencyContactService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create Emergency Contact",
    description="Create new emergency contact record for an employee"
)
async def create_emergency_contact(
    emergency_contact: EmergencyContactCreate,
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new emergency contact.
    
    Args:
        emergency_contact: Emergency contact data to create
        service: Emergency contacts service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with created emergency contact
    """
    # Set employee_id from current user
    emergency_contact.employee_id = current_user['employee_id']
    created_contact = await service.create_emergency_contact(db, emergency_contact)
    response_data = EmergencyContactResponse.model_validate(created_contact)
    
    return success_response(
        data=response_data, 
        message=response_message.CREATED_SUCCESS, 
        code=status.HTTP_201_CREATED
    )


@router.get(
    "/{contact_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Emergency Contact by ID",
    description="Retrieve emergency contact by contact ID"
)
async def get_emergency_contact_by_id(
    contact_id: str = Path(..., description="Emergency contact unique identifier"),
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get emergency contact by contact ID.
    
    Args:
        contact_id: Emergency contact unique identifier
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response with emergency contact data
    """
    print("----------------------------------------wooo--------")
    emergency_contact = await service.get_emergency_contact_by_id(db, contact_id)
    response_data = EmergencyContactResponse.model_validate(emergency_contact)
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Emergency Contacts by Employee ID",
    description="Retrieve all emergency contacts for current employee"
)
async def get_emergency_contacts_by_employee_id(
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get emergency contacts by employee ID.
    
    Args:
        service: Emergency contacts service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with emergency contacts list
    """
    emergency_contacts = await service.get_emergency_contacts_by_employee_id(
        db, current_user['employee_id']
    )
    response_data = [EmergencyContactResponse.model_validate(contact) for contact in emergency_contacts]
    
    return success_response(
        data=response_data,
        message=response_message.SUCCESS,
        code=status.HTTP_200_OK
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get All Emergency Contacts",
    description="Retrieve all emergency contacts with pagination"
)
async def get_all_emergency_contacts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all emergency contacts with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response with list of emergency contacts and metadata
    """
    print("------------------------------------------this black hat------------")
    emergency_contacts_list = await service.get_all_emergency_contacts(db, skip, limit)
    total_count = await service.get_emergency_contacts_count(db)
    
    response_data = {
        "items": [EmergencyContactResponse.model_validate(item) for item in emergency_contacts_list],
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
    "/{contact_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Update Emergency Contact",
    description="Update emergency contact by ID"
)
async def update_emergency_contact(
    update_data: EmergencyContactUpdate,
    contact_id: str = Path(..., description="Emergency contact unique identifier"),
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Update emergency contact.
    
    Args:
        update_data: Data to update
        contact_id: Emergency contact unique identifier
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response with updated emergency contact
    """
    updated_contact = await service.update_emergency_contact(db, contact_id, update_data)
    response_data = EmergencyContactResponse.model_validate(updated_contact)
    
    return success_response(
        data=response_data,
        message=response_message.UPDATED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete Emergency Contact",
    description="Delete emergency contact by ID"
)
async def delete_emergency_contact(
    contact_id: str = Path(..., description="Emergency contact unique identifier"),
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete emergency contact.
    
    Args:
        contact_id: Emergency contact unique identifier
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response confirming deletion
    """
    await service.delete_emergency_contact(db, contact_id)
    
    return success_response(
        data={"deleted": True, "contact_id": contact_id},
        message=response_message.DELETED_SUCCESS,
        code=status.HTTP_200_OK
    )


@router.delete(
    "/employee/my/all",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete All Emergency Contacts for Employee",
    description="Delete all emergency contacts for current employee"
)
async def delete_all_emergency_contacts_by_employee_id(
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete all emergency contacts for current employee.
    
    Args:
        service: Emergency contacts service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with deletion count
    """
    deleted_count = await service.delete_all_emergency_contacts_by_employee_id(
        db, current_user['employee_id']
    )
    
    return success_response(
        data={"deleted_count": deleted_count, "employee_id": current_user['employee_id']},
        message=f"Deleted {deleted_count} emergency contacts",
        code=status.HTTP_200_OK
    )


@router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Search Emergency Contacts",
    description="Search emergency contacts by name or phone number"
)
async def search_emergency_contacts(
    q: str = Query(..., min_length=2, description="Search term (name or phone)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Search emergency contacts by name or phone number.
    
    Args:
        q: Search term (minimum 2 characters)
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response with search results
    """
    search_results = await service.search_emergency_contacts(db, q, skip, limit)
    
    response_data = {
        "items": [EmergencyContactResponse.model_validate(item) for item in search_results],
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
    summary="Get Emergency Contacts Count",
    description="Get total count of emergency contacts records"
)
async def get_emergency_contacts_count(
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Get total count of emergency contacts records.
    
    Args:
        service: Emergency contacts service instance
        db: Database session
        
    Returns:
        Success response with count information
    """
    total_count = await service.get_emergency_contacts_count(db)
    
    return success_response(
        data={"total_records": total_count},
        message="Count retrieved successfully",
        code=status.HTTP_200_OK
    )


@router.get(
    "/employee/my/count",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Get Emergency Contacts Count for Employee",
    description="Get count of emergency contacts for current employee"
)
async def get_emergency_contacts_count_by_employee_id(
    service: EmergencyContactService = Depends(get_emergency_contacts_service),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get count of emergency contacts for current employee.
    
    Args:
        service: Emergency contacts service instance
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success response with count information
    """
    count = await service.get_emergency_contacts_count_by_employee_id(
        db, current_user['employee_id']
    )
    
    return success_response(
        data={"employee_id": current_user['employee_id'], "contact_count": count},
        message="Employee contact count retrieved successfully",
        code=status.HTTP_200_OK
    )